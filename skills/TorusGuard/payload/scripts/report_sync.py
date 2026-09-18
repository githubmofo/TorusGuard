#!/usr/bin/env python3
"""
TorusGuard Living Security Report Sync Engine (v1.3.6)
Maintains a living, ground-truth `security_report.md` ledger at the root of the workspace.
Tracks finding lifecycles from Discovery -> Candidate -> Applied -> Resolved -> Regressed.
Pure Python 3.10+ standard library (zero external dependencies).
"""

import sys
import os
import re
import json
import time
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Windows console UTF-8 support
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        getattr(sys.stdout, "reconfigure")(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        getattr(sys.stderr, "reconfigure")(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Timezone: Indian Standard Time (IST, UTC+05:30)
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30), name="IST")

def get_ist_now() -> datetime.datetime:
    """Return timezone-aware datetime in IST."""
    return datetime.datetime.now(IST)

def format_timestamp(dt: Optional[datetime.datetime] = None) -> str:
    if dt is None:
        dt = get_ist_now()
    return dt.strftime("%Y-%m-%d %H:%M:%S IST")

def get_report_path(target_root: Path) -> Path:
    """Return absolute path to security_report.md at the workspace root."""
    return target_root / "security_report.md"


def atomic_write_text(file_path: Path, content: str, max_retries: int = 3, backoff_base: float = 0.05) -> bool:
    """
    Atomically write text to disk using a temporary file and atomic replace.
    Handles Windows file-locking (e.g. browser read locks on open HTML reports)
    via exponential backoff retries.
    """
    file_path = Path(file_path).resolve()
    file_path.parent.mkdir(parents=True, exist_ok=True)

    pid = os.getpid()
    ts = int(time.time() * 1000)
    tmp_path = file_path.with_name(f".tmp.{pid}.{ts}.{file_path.name}")

    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
    except Exception as e:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except Exception:
                pass
        raise e

    for attempt in range(max_retries):
        try:
            os.replace(tmp_path, file_path)
            return True
        except (PermissionError, OSError):
            if attempt == max_retries - 1:
                try:
                    file_path.write_text(content, encoding="utf-8")
                    if tmp_path.exists():
                        tmp_path.unlink()
                    return True
                except Exception:
                    if tmp_path.exists():
                        try:
                            tmp_path.unlink()
                        except Exception:
                            pass
                    raise
            time.sleep(backoff_base * (2 ** attempt))

    return False


def reconcile_from_run_artifacts(target_root: Path) -> List[Dict[str, Any]]:
    """
    Authoritative fallback: if security_report.md is missing or damaged,
    heal state from the latest run's findings.json in .torusguard/runs/.
    """
    runs_dir = target_root / ".torusguard" / "runs"
    if not runs_dir.is_dir():
        return []

    run_folders = sorted(
        [d for d in runs_dir.iterdir() if d.is_dir() and (d / "findings.json").is_file()],
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    if not run_folders:
        return []

    latest_file = run_folders[0] / "findings.json"
    try:
        data = json.loads(latest_file.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return []


def parse_existing_report(report_path: Path) -> Dict[str, Any]:
    """Parse existing security_report.md into structured data if it exists.
    Supports both the legacy format and the new v2 summary-first format.
    Heals from latest run findings if report is absent or damaged.
    """
    if not report_path.is_file():
        recovered = reconcile_from_run_artifacts(report_path.parent)
        if recovered:
            f_map = {}
            for r in recovered:
                fid = r.get("finding_id", "")
                if fid:
                    f_map[fid] = {
                        "finding_id": fid,
                        "rule_id": r.get("rule_id", "TG-GEN"),
                        "title": r.get("title", "Security Finding"),
                        "status": "🔴 OPEN",
                        "severity": r.get("severity", "Medium"),
                        "confidence": f"{r.get('confidence_score', 70)}% ({r.get('confidence_band', 'High Confidence')})",
                        "target": f"{r.get('file_path', '')}:{r.get('line_number', 1)}",
                        "history": []
                    }
            return {"findings": f_map, "metadata": {}}
        return {"findings": {}, "metadata": {}}
    
    try:
        content = report_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {"findings": {}, "metadata": {}}

    findings = {}

    # ── Format A (legacy): ### [RULE-ID] Title ──
    card_pattern_legacy = re.compile(
        r'###\s+\[(TG-[A-Z]+-\d+)\]\s+(.*?)\n'
        r'- \*\*Finding ID:\*\*\s+`([^`]+)`\n'
        r'- \*\*Status:\*\*\s+([^\n]+)\n'
        r'- \*\*Severity:\*\*\s+([^\n|]+)(?:\|\s+\*\*Confidence:\*\*\s+([^\n]+))?\n'
        r'- \*\*Target:\*\*\s+`([^`]+)`',
        re.MULTILINE
    )

    for m in card_pattern_legacy.finditer(content):
        rule_id = m.group(1).strip()
        title = m.group(2).strip()
        finding_id = m.group(3).strip()
        status = m.group(4).strip()
        severity = m.group(5).strip()
        confidence = m.group(6).strip() if m.group(6) else "70% (High Confidence)"
        target = m.group(7).strip()

        findings[finding_id] = {
            "finding_id": finding_id,
            "rule_id": rule_id,
            "title": title,
            "status": status,
            "severity": severity,
            "confidence": confidence,
            "target": target,
            "history": []
        }

    # ── Format B (new v2): ### TG-RULE-001 · Title `status` `confidence` ──
    card_pattern_v2 = re.compile(
        r'###\s+(TG-[A-Z]+-\d+)\s+·\s+(.*?)\s+`([^`]+)`\s+`([^`]+)`\n'
        r'- \*\*Finding ID:\*\*\s+`([^`]+)`(?:[^\n]*\*\*Severity:\*\*\s+`([^`]+)`)?\n'
        r'(?:📁|- \*\*Target:\*\*)\s*`([^`\n]+)`',
        re.MULTILINE
    )

    for m in card_pattern_v2.finditer(content):
        rule_id = m.group(1).strip()
        title = m.group(2).strip()
        status = m.group(3).strip()
        confidence = m.group(4).strip()
        finding_id = m.group(5).strip()
        sev_explicit = m.group(6).strip() if m.group(6) else None
        target = m.group(7).strip()

        if finding_id not in findings:  # Don't overwrite legacy matches
            if sev_explicit:
                severity = sev_explicit
            else:
                # Infer severity from section header or status
                severity = "High"  # Default
                match_pos = m.start()
                preceding = content[:match_pos]
                if "Critical" in preceding.split("##")[-1]:
                    severity = "Critical"
                elif "Medium" in preceding.split("##")[-1]:
                    severity = "Medium"

            findings[finding_id] = {
                "finding_id": finding_id,
                "rule_id": rule_id,
                "title": title,
                "status": status,
                "severity": severity,
                "confidence": confidence,
                "target": target,
                "history": []
            }

    # Extract history from inline blockquote format (new) or table format (legacy)
    # Legacy: #### Lifecycle History for `finding_id`
    history_pattern = re.compile(r'#### Lifecycle History for `([^`]+)`\n([\s\S]*?)(?=\n---|\n###|\Z)')
    for hm in history_pattern.finditer(content):
        fid = hm.group(1).strip()
        table_text = hm.group(2).strip()
        if fid in findings:
            for row in table_text.splitlines():
                if row.startswith("|") and not row.startswith("| Timestamp"):
                    cols = [c.strip().strip("`") for c in row.split("|")[1:-1]]
                    if len(cols) >= 4 and not cols[0].startswith(":") and not cols[0].startswith("-"):
                        findings[fid]["history"].append({
                            "timestamp": cols[0],
                            "action": cols[1],
                            "run_id": cols[2],
                            "details": cols[3]
                        })

    # New format: > Last: Action — timestamp · `run_id`
    inline_history = re.compile(
        r'###\s+TG-[A-Z]+-\d+.*?\n.*?Finding ID:\*\*\s+`([^`]+)`.*?'
        r'>\s+Last:\s+(.*?)\s+—\s+(.*?)\s+·\s+`([^`]+)`',
        re.DOTALL
    )
    for hm in inline_history.finditer(content):
        fid = hm.group(1).strip()
        if fid in findings and not findings[fid]["history"]:
            findings[fid]["history"].append({
                "timestamp": hm.group(3).strip(),
                "action": hm.group(2).strip(),
                "run_id": hm.group(4).strip(),
                "details": "Restored from inline history"
            })


    return {"findings": findings, "raw_content": content}


def parse_metadata_block(content: str) -> Dict[str, Any]:
    """Parse the YAML metadata block between TORUSGUARD_METADATA_START/END markers."""
    metadata = {}
    meta_match = re.search(
        r'<!-- TORUSGUARD_METADATA_START\s*\n(.*?)\nTORUSGUARD_METADATA_END -->',
        content, re.DOTALL
    )
    if meta_match:
        for line in meta_match.group(1).strip().splitlines():
            if ':' in line:
                key, _, val = line.partition(':')
                metadata[key.strip()] = val.strip()
    return metadata

def compute_health_score(findings: List[Dict[str, Any]]) -> Tuple[int, str]:
    """
    Compute security health score (0-100) based on remaining open/regressed findings.
    Returns (score, status_text).
    """
    critical_count = sum(1 for f in findings if f["severity"].lower() == "critical" and ("OPEN" in f["status"] or "REGRESSED" in f["status"]))
    high_count = sum(1 for f in findings if f["severity"].lower() == "high" and ("OPEN" in f["status"] or "REGRESSED" in f["status"]))
    medium_count = sum(1 for f in findings if f["severity"].lower() == "medium" and ("OPEN" in f["status"] or "REGRESSED" in f["status"]))
    low_count = sum(1 for f in findings if f["severity"].lower() == "low" and ("OPEN" in f["status"] or "REGRESSED" in f["status"]))

    penalty = (critical_count * 25) + (high_count * 15) + (medium_count * 5) + (low_count * 2)
    score = max(0, min(100, 100 - penalty))

    if score == 100:
        status = "🟢 HARDENED & SECURE"
    elif score >= 80:
        status = "🟡 MODERATE RISK — ACTION RECOMMENDED"
    elif score >= 50:
        status = "🟠 ELEVATED RISK — PATCHES REQUIRED"
    else:
        status = "🔴 CRITICAL RISK — IMMEDIATE INTERVENTION REQUIRED"

    return score, status

def render_report(findings: List[Dict[str, Any]], target_root: Path) -> str:
    """Render the living security_report.md with summary-first layout,
    AI-parseable metadata, severity grouping, and concise finding cards."""
    score, status_text = compute_health_score(findings)
    now_str = format_timestamp()

    # Counts
    total = len(findings)
    open_count = sum(1 for f in findings if "OPEN" in f["status"])
    verified_count = sum(1 for f in findings if "VERIFIED" in f["status"])
    candidate_count = sum(1 for f in findings if "CANDIDATE" in f["status"])
    applied_count = sum(1 for f in findings if "APPLIED" in f["status"])
    resolved_count = sum(1 for f in findings if "RESOLVED" in f["status"])
    regressed_count = sum(1 for f in findings if "REGRESSED" in f["status"])
    fp_count = sum(1 for f in findings if "FALSE POSITIVE" in f["status"])

    crit_count = sum(1 for f in findings if f["severity"].lower() == "critical")
    high_count = sum(1 for f in findings if f["severity"].lower() == "high")
    med_count = sum(1 for f in findings if f["severity"].lower() == "medium")
    low_count = sum(1 for f in findings if f["severity"].lower() == "low")

    crit_open = sum(1 for f in findings if f["severity"].lower() == "critical" and ("OPEN" in f["status"] or "REGRESSED" in f["status"]))
    high_open = sum(1 for f in findings if f["severity"].lower() == "high" and ("OPEN" in f["status"] or "REGRESSED" in f["status"]))
    med_open = sum(1 for f in findings if f["severity"].lower() == "medium" and ("OPEN" in f["status"] or "REGRESSED" in f["status"]))

    # Sort findings by status priority and severity
    sev_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    def sort_key(f):
        is_active = 0 if ("OPEN" in f["status"] or "REGRESSED" in f["status"]) else 1
        s_rank = sev_rank.get(f["severity"].lower(), 9)
        return (is_active, s_rank, f["rule_id"])

    sorted_findings = sorted(findings, key=sort_key)

    # Group by severity for active findings
    active = [f for f in sorted_findings if "OPEN" in f["status"] or "REGRESSED" in f["status"]]
    resolved = [f for f in sorted_findings if "RESOLVED" in f["status"]]
    in_progress = [f for f in sorted_findings if any(s in f["status"] for s in ("CANDIDATE", "APPLIED", "VERIFIED"))]
    suppressed = [f for f in sorted_findings if "FALSE POSITIVE" in f["status"]]

    critical_findings = [f for f in active if f["severity"].lower() == "critical"]
    high_findings = [f for f in active if f["severity"].lower() == "high"]
    medium_findings = [f for f in active if f["severity"].lower() in ("medium", "low")]

    # ── Build the report ──
    lines = [
        "# 🛡️ TorusGuard Security Report",
        "",
        "<!-- TORUSGUARD_METADATA_START",
        f"health_score: {score}",
        f"status: {status_text}",
        f"total_findings: {total}",
        f"critical: {crit_count}",
        f"critical_open: {crit_open}",
        f"high: {high_count}",
        f"high_open: {high_open}",
        f"medium: {med_count}",
        f"medium_open: {med_open}",
        f"low: {low_count}",
        f"open: {open_count}",
        f"resolved: {resolved_count}",
        f"regressed: {regressed_count}",
        f"suppressed: {fp_count}",
        f"last_scan: {now_str}",
        "TORUSGUARD_METADATA_END -->",
        "",
        "## Executive Summary",
        "",
        "| Metric | Value |",
        "| :--- | :--- |",
        f"| **Health Score** | `{score}/100` — {status_text} |",
        f"| **Critical (Open)** | {crit_open} |",
        f"| **High (Open)** | {high_open} |",
        f"| **Medium (Open)** | {med_open} |",
        f"| **Resolved** | {resolved_count} |",
        f"| **In Progress** | {candidate_count + applied_count} |",
        f"| **Last Scan** | {now_str} |",
        "",
    ]

    # Action required callout
    if crit_open > 0:
        lines.append(f"> ⚠️ **Action Required:** {crit_open} critical finding{'s' if crit_open != 1 else ''} require immediate attention. Run `npx torusguard harden` to generate patches.")
        lines.append("")

    lines.append("---")
    lines.append("")

    # ── Critical Findings Section ──
    if critical_findings:
        lines.append(f"## 🔴 Critical Findings ({len(critical_findings)})")
        lines.append("")
        for f in critical_findings:
            lines.extend(_render_finding_card(f))
    
    # ── High Findings Section ──
    if high_findings:
        lines.append(f"## 🟠 High Findings ({len(high_findings)})")
        lines.append("")
        for f in high_findings:
            lines.extend(_render_finding_card(f))

    # ── Medium/Low Findings Section ──
    if medium_findings:
        lines.append(f"## 🟡 Medium / Low Findings ({len(medium_findings)})")
        lines.append("")
        for f in medium_findings:
            lines.extend(_render_finding_card(f))

    # ── In Progress Section ──
    if in_progress:
        lines.append(f"## 🔵 In Progress ({len(in_progress)})")
        lines.append("")
        for f in in_progress:
            lines.extend(_render_finding_card(f))

    # ── Resolved Section ──
    if resolved:
        lines.append(f"## ✅ Resolved ({len(resolved)})")
        lines.append("")
        for f in resolved:
            lines.extend(_render_finding_card(f))

    # ── Suppressed Section ──
    if suppressed:
        lines.append(f"## ⚪ Suppressed ({len(suppressed)})")
        lines.append("")
        for f in suppressed:
            lines.append(f"- **{f['rule_id']}** · {f['title']} — `{f['target']}` · False Positive")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Footer
    lines.append("---")
    lines.append(f"*Generated by TorusGuard v1.3.6 · {now_str} · 100% Local-First*")
    lines.append("")

    return "\n".join(lines)


def _render_finding_card(f: Dict[str, Any]) -> List[str]:
    """Render a concise finding card (4-6 lines max)."""
    status_full = f["status"]
    conf = f.get('confidence', '70% (High Confidence)')
    sev = f.get('severity', 'High')
    card = [
        f"### {f['rule_id']} · {f['title']} `{status_full}` `{conf}`",
        f"- **Finding ID:** `{f['finding_id']}` · **Severity:** `{sev}`",
        f"📁 `{f['target']}`",
        f"**Problem:** {f.get('what_is_wrong', f.get('description', 'Security violation detected.'))}",
    ]
    if f.get("what_should_change"):
        card.append(f"**Fix:** {f['what_should_change']}")
    if f.get("proposed_diff"):
        card.append("")
        card.append("```diff")
        card.append(f["proposed_diff"].strip())
        card.append("```")
    card.append("")
    # Include lifecycle history inline (compact)
    history = f.get("history", [])
    if history and len(history) > 0:
        last_event = history[-1]
        card.append(f"> Last: {last_event.get('action', '?')} — {last_event.get('timestamp', '?')} · `{last_event.get('run_id', '?')}`")
        card.append("")
    card.append("---")
    card.append("")
    return card


def record_audit_findings(target_root: Path, findings: List[Dict[str, Any]], run_id: str):
    """
    Called at the conclusion of `npx torusguard audit`.
    Updates security_report.md with new findings or records re-appearance.
    """
    report_file = get_report_path(target_root)
    existing = parse_existing_report(report_file)
    existing_map = existing["findings"]

    now_str = format_timestamp()
    current_fids = set()

    for f in findings:
        fid = f.get("finding_id", f"{f['rule_id']}-{f['line_number']}")
        current_fids.add(fid)
        rel_target = f"{f['file_path']}:{f['line_number']}"

        if fid in existing_map:
            # Finding already known
            item = existing_map[fid]
            item["target"] = rel_target
            item["snippet"] = f.get("snippet", "")
            item["description"] = f.get("description", "")

            # If it was RESOLVED or APPLIED and reappeared, mark as REGRESSED
            if "RESOLVED" in item["status"] or "APPLIED" in item["status"]:
                item["status"] = "❌ REGRESSED"
                item["history"].append({
                    "timestamp": now_str,
                    "action": "Regression Detected",
                    "run_id": run_id,
                    "details": "Vulnerability pattern re-detected in source code after prior closure."
                })
        else:
            # Brand new finding
            conf_str = f"{f.get('confidence_score', 70)}% ({f.get('confidence_band', 'High Confidence')})"
            existing_map[fid] = {
                "finding_id": fid,
                "rule_id": f["rule_id"],
                "title": f["title"],
                "status": "🔴 OPEN",
                "severity": f["severity"],
                "confidence": conf_str,
                "target": rel_target,
                "cluster": f.get("cluster", "cluster-general"),
                "what_is_wrong": f.get("description", ""),
                "why_it_matters": "Violates TorusGuard strict production safety and isolation invariant.",
                "what_should_change": f"Apply Ponytail-compliant patch via `npx torusguard harden`.",
                "snippet": f.get("snippet", ""),
                "history": [{
                    "timestamp": now_str,
                    "action": "Discovered",
                    "run_id": run_id,
                    "details": f"Initial discovery during static AST audit in {f['file_path']}."
                }]
            }

    # For findings in existing report that were OPEN, APPLIED, or CANDIDATE and no longer detected, transition to RESOLVED
    for fid, item in existing_map.items():
        if fid not in current_fids and ("OPEN" in item["status"] or "APPLIED" in item["status"] or "CANDIDATE" in item["status"]):
            item["status"] = "🟢 RESOLVED"
            item["history"].append({
                "timestamp": now_str,
                "action": "Resolved",
                "run_id": run_id,
                "details": "Finding no longer detected in source code during latest audit pass."
            })

    # Render and save
    rendered = render_report(list(existing_map.values()), target_root)
    atomic_write_text(report_file, rendered)
    sync_html_if_exists(target_root)
    return report_file


def record_harden_bundles(target_root: Path, bundles: List[Dict[str, Any]], run_id: str):
    """
    Called at the conclusion of `npx torusguard harden`.
    Transitions findings to CANDIDATE 🟡 and attaches minimal patch diff previews.
    """
    report_file = get_report_path(target_root)
    existing = parse_existing_report(report_file)
    existing_map = existing["findings"]
    now_str = format_timestamp()

    for b in bundles:
        fid = b.get("finding_id")
        rule_id = b.get("rule_id")
        target = f"{b['target_file']}:{b['line_number']}"

        # Match by finding_id or target
        matched_item = None
        if fid and fid in existing_map:
            matched_item = existing_map[fid]
        else:
            for item in existing_map.values():
                if item["rule_id"] == rule_id and item["target"] == target:
                    matched_item = item
                    break

        if matched_item:
            matched_item["status"] = "🟡 CANDIDATE"
            matched_item["what_should_change"] = b.get("what_should_change", "")
            matched_item["proposed_diff"] = b.get("proposed_diff", "")
            matched_item["bundle_id"] = b.get("bundle_id", "")
            matched_item["history"].append({
                "timestamp": now_str,
                "action": "Patch Formulated",
                "run_id": run_id,
                "details": f"Ponytail candidate bundle {b.get('bundle_id')} formulated (+{b.get('additions', 0)} / -{b.get('deletions', 0)} lines)."
            })

    rendered = render_report(list(existing_map.values()), target_root)
    atomic_write_text(report_file, rendered)
    sync_html_if_exists(target_root)
    return report_file


def record_applied_patches(target_root: Path, applied_bundles: List[Dict[str, Any]], snapshot_dir: Path, run_id: str):
    """
    Called at the conclusion of `npx torusguard apply`.
    Transitions findings to APPLIED 🔵 and records snapshot path.
    """
    report_file = get_report_path(target_root)
    existing = parse_existing_report(report_file)
    existing_map = existing["findings"]
    now_str = format_timestamp()

    for b in applied_bundles:
        fid = b.get("finding_id")
        rule_id = b.get("rule_id")
        target = f"{b.get('target_file', '')}:{b.get('line_number', '')}"

        matched_item = None
        if fid and fid in existing_map:
            matched_item = existing_map[fid]
        else:
            for item in existing_map.values():
                if item["rule_id"] == rule_id and (target in item["target"] or item["target"] in target):
                    matched_item = item
                    break

        if matched_item:
            matched_item["status"] = "🔵 APPLIED"
            matched_item["history"].append({
                "timestamp": now_str,
                "action": "Patch Applied",
                "run_id": run_id,
                "details": f"Candidate patch applied to disk. Pre-apply snapshot saved in {snapshot_dir.name}."
            })

    rendered = render_report(list(existing_map.values()), target_root)
    atomic_write_text(report_file, rendered)
    sync_html_if_exists(target_root)
    return report_file


def record_recheck_results(target_root: Path, recheck_results: Dict[str, Any], run_id: str):
    """
    Called at the conclusion of `npx torusguard recheck` or `verify`.
    Transitions findings to RESOLVED 🟢 or REGRESSED ❌.
    """
    report_file = get_report_path(target_root)
    existing = parse_existing_report(report_file)
    existing_map = existing["findings"]
    now_str = format_timestamp()

    fixed = recheck_results.get("fixed", [])
    regressed = recheck_results.get("regressed", [])
    remaining = recheck_results.get("remaining", [])

    for f in fixed:
        fid = f.get("finding_id")
        if fid and fid in existing_map:
            existing_map[fid]["status"] = "🟢 RESOLVED"
            existing_map[fid]["history"].append({
                "timestamp": now_str,
                "action": "Closure Verified",
                "run_id": run_id,
                "details": "Targeted differential AST re-scan verified fix closure. Zero regressions."
            })

    for r in regressed:
        fid = r.get("finding_id")
        if fid and fid in existing_map:
            existing_map[fid]["status"] = "❌ REGRESSED"
            existing_map[fid]["history"].append({
                "timestamp": now_str,
                "action": "Regression Detected",
                "run_id": run_id,
                "details": "Vulnerability or new issue detected during recheck pass."
            })

    rendered = render_report(list(existing_map.values()), target_root)
    atomic_write_text(report_file, rendered)
    sync_html_if_exists(target_root)
    return report_file


def record_rollback_results(target_root: Path, restored_files: List[str], run_id: str):
    """
    Called at the conclusion of `npx torusguard rollback`.
    Reverts findings for restored files back to OPEN 🔴.
    """
    report_file = get_report_path(target_root)
    existing = parse_existing_report(report_file)
    existing_map = existing["findings"]
    now_str = format_timestamp()

    norm_restored = {rf.replace("\\", "/") for rf in restored_files}

    for item in existing_map.values():
        target_path = item.get("target", "").split(":")[0].replace("\\", "/")
        if any(rf in target_path or target_path in rf for rf in norm_restored):
            item["status"] = "🔴 OPEN"
            item["history"].append({
                "timestamp": now_str,
                "action": "Rollback Restored",
                "run_id": run_id,
                "details": f"File {target_path} reverted from pre-apply snapshot. Status restored to OPEN."
            })

    rendered = render_report(list(existing_map.values()), target_root)
    atomic_write_text(report_file, rendered)
    sync_html_if_exists(target_root)
    return report_file


def sync_html_if_exists(target_root: Path):
    """
    If the user has already generated report.html (at root or in .torusguard/runs),
    refresh it so the HTML dashboard stays in lockstep with security_report.md.
    """
    root_html = target_root / "report.html"
    runs_html = target_root / ".torusguard" / "runs" / "report-latest.html"
    if root_html.is_file() or runs_html.is_file():
        try:
            s_dir = Path(__file__).resolve().parent
            if str(s_dir) not in sys.path:
                sys.path.insert(0, str(s_dir))
            import html_reporter
            if runs_html.is_file():
                html_reporter.emit_html_report(target_path=runs_html, root_dir=target_root)
            if root_html.is_file():
                html_reporter.emit_html_report(target_path=root_html, root_dir=target_root)
        except Exception:
            pass
