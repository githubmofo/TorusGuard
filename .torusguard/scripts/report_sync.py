#!/usr/bin/env python3
"""
TorusGuard Living Security Report Sync Engine (v1.3.5)
Maintains a living, ground-truth `security_report.md` ledger at the root of the workspace.
Tracks finding lifecycles from Discovery -> Candidate -> Applied -> Resolved -> Regressed.
Pure Python 3.10+ standard library (zero external dependencies).
"""

import sys
import os
import re
import json
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

def parse_existing_report(report_path: Path) -> Dict[str, Any]:
    """Parse existing security_report.md into structured data if it exists."""
    if not report_path.is_file():
        return {"findings": {}, "metadata": {}}
    
    try:
        content = report_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {"findings": {}, "metadata": {}}

    findings = {}
    # Parse individual finding cards: ### [RULE-ID] Title
    card_pattern = re.compile(
        r'###\s+\[(TG-[A-Z]+-\d+)\]\s+(.*?)\n'
        r'- \*\*Finding ID:\*\*\s+`([^`]+)`\n'
        r'- \*\*Status:\*\*\s+([^\n]+)\n'
        r'- \*\*Severity:\*\*\s+([^\n|]+)(?:\|\s+\*\*Confidence:\*\*\s+([^\n]+))?\n'
        r'- \*\*Target:\*\*\s+`([^`]+)`',
        re.MULTILINE
    )

    for m in card_pattern.finditer(content):
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

    # Extract history tables if present
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

    return {"findings": findings, "raw_content": content}

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
    """Render the full living security_report.md document."""
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

    lines = [
        "# 🛡️ TorusGuard Living Security Report",
        "",
        "> **Notice:** This document is the living, single-source-of-truth ledger for security findings,",
        "> candidate patches, and verified closures across this repository. Updated automatically by",
        "> TorusGuard CLI commands (`audit`, `harden`, `apply`, `recheck`) and AI chat workflows.",
        "",
        "---",
        "",
        "## 📊 Security Posture Overview",
        "",
        f"- **Health Score:** `{score}/100` — **{status_text}**",
        f"- **Last Updated:** `{now_str}`",
        f"- **Total Tracked Findings:** `{total}`",
        f"- **Status Breakdown:** `🔴 {open_count} Open` · `🟠 {verified_count} Verified` · `🟡 {candidate_count} Candidate` · `🔵 {applied_count} Applied` · `🟢 {resolved_count} Resolved` · `❌ {regressed_count} Regressed` · `⚪ {fp_count} Suppressed`",
        "",
        "| Severity | Total | Open / Regressed | Resolved | Candidate / Applied |",
        "| :--- | :---: | :---: | :---: | :---: |",
        f"| **Critical** | {crit_count} | {sum(1 for f in findings if f['severity'].lower() == 'critical' and ('OPEN' in f['status'] or 'REGRESSED' in f['status']))} | {sum(1 for f in findings if f['severity'].lower() == 'critical' and 'RESOLVED' in f['status'])} | {sum(1 for f in findings if f['severity'].lower() == 'critical' and ('CANDIDATE' in f['status'] or 'APPLIED' in f['status']))} |",
        f"| **High** | {high_count} | {sum(1 for f in findings if f['severity'].lower() == 'high' and ('OPEN' in f['status'] or 'REGRESSED' in f['status']))} | {sum(1 for f in findings if f['severity'].lower() == 'high' and 'RESOLVED' in f['status'])} | {sum(1 for f in findings if f['severity'].lower() == 'high' and ('CANDIDATE' in f['status'] or 'APPLIED' in f['status']))} |",
        f"| **Medium** | {med_count} | {sum(1 for f in findings if f['severity'].lower() == 'medium' and ('OPEN' in f['status'] or 'REGRESSED' in f['status']))} | {sum(1 for f in findings if f['severity'].lower() == 'medium' and 'RESOLVED' in f['status'])} | {sum(1 for f in findings if f['severity'].lower() == 'medium' and ('CANDIDATE' in f['status'] or 'APPLIED' in f['status']))} |",
        f"| **Low** | {low_count} | {sum(1 for f in findings if f['severity'].lower() == 'low' and ('OPEN' in f['status'] or 'REGRESSED' in f['status']))} | {sum(1 for f in findings if f['severity'].lower() == 'low' and 'RESOLVED' in f['status'])} | {sum(1 for f in findings if f['severity'].lower() == 'low' and ('CANDIDATE' in f['status'] or 'APPLIED' in f['status']))} |",
        "",
        "---",
        "",
        "## 🔍 Tracked Findings Detail",
        ""
    ]

    # Sort findings: Open/Regressed first, then by severity (Critical -> High -> Medium -> Low), then rule_id
    sev_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    def sort_key(f):
        is_active = 0 if ("OPEN" in f["status"] or "REGRESSED" in f["status"]) else 1
        s_rank = sev_rank.get(f["severity"].lower(), 9)
        return (is_active, s_rank, f["rule_id"])

    sorted_findings = sorted(findings, key=sort_key)

    for f in sorted_findings:
        lines.append(f"### [{f['rule_id']}] {f['title']}")
        lines.append(f"- **Finding ID:** `{f['finding_id']}`")
        lines.append(f"- **Status:** {f['status']}")
        lines.append(f"- **Severity:** {f['severity']} | **Confidence:** {f.get('confidence', '70% (High Confidence)')}")
        lines.append(f"- **Target:** `{f['target']}`")
        if f.get("cluster"):
            lines.append(f"- **Root-Cause Cluster:** `{f['cluster']}`")
        lines.append("")
        lines.append(f"**What is wrong:**  \n{f.get('what_is_wrong', f.get('description', 'Security violation detected by TorusGuard scanner.'))}")
        lines.append("")
        lines.append(f"**Why it matters:**  \n{f.get('why_it_matters', 'Violates TorusGuard strict production safety and isolation invariant.')}")
        lines.append("")
        if f.get("what_should_change"):
            lines.append(f"**Governed Remediation:**  \n{f['what_should_change']}")
            lines.append("")
        if f.get("snippet"):
            lines.append("```")
            lines.append(f["snippet"].strip())
            lines.append("```")
            lines.append("")
        if f.get("proposed_diff"):
            lines.append("**Proposed Minimal Patch Preview (Ponytail Bounded):**")
            lines.append("```diff")
            lines.append(f["proposed_diff"].strip())
            lines.append("```")
            lines.append("")

        # History table
        history = f.get("history", [])
        if history:
            lines.append(f"#### Lifecycle History for `{f['finding_id']}`")
            lines.append("| Timestamp | Action | Run ID | Details |")
            lines.append("| :--- | :--- | :--- | :--- |")
            for h in history:
                lines.append(f"| {h['timestamp']} | {h['action']} | `{h['run_id']}` | {h['details']} |")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


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
    report_file.write_text(rendered, encoding="utf-8")
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
    report_file.write_text(rendered, encoding="utf-8")
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
    report_file.write_text(rendered, encoding="utf-8")
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
    report_file.write_text(rendered, encoding="utf-8")
    return report_file
