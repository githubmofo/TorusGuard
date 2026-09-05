#!/usr/bin/env python3
"""
TorusGuard Adaptive Security Memory Engine (v1.0.0)
Zero-dependency persistent intelligence layer for local-first security guardrails.
Manages raw event logging, pattern distillation, confidence amplification/decay,
and token-budgeted context window computation for AI agent prompts.
"""

import os
import sys
import json
import datetime
import hashlib
import uuid
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Ensure UTF-8 stdout/stderr on Windows consoles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

VERSION = "1.0.0"
DEFAULT_TOKEN_BUDGET = 2000
DEFAULT_TTL_DAYS = 90
DEFAULT_DECAY_RATE = 0.15


def find_project_root(start_dir: Optional[str] = None) -> Path:
    """Detect project root directory by searching for standard repo root markers."""
    current = Path(start_dir or os.getcwd()).resolve()
    markers = [".git", "package.json", "pyproject.toml", "manage.py", "Pipfile", "requirements.txt", ".torusguard"]

    for m in markers:
        if (current / m).exists():
            return current

    for parent in current.parents:
        for m in markers:
            if (parent / m).exists():
                return parent

    return current


def get_memory_paths(root_dir: Optional[Path] = None) -> Dict[str, Path]:
    """Return all key paths within the .torusguard/memory subsystem."""
    base = Path(root_dir or find_project_root()).resolve()
    torusguard_dir = base / ".torusguard"
    memory_dir = torusguard_dir / "memory"
    events_dir = memory_dir / "events"

    return {
        "root": base,
        "torusguard": torusguard_dir,
        "memory": memory_dir,
        "events": events_dir,
        "patterns": memory_dir / "patterns.json",
        "context": memory_dir / "context.json",
        "profile": memory_dir / "profile.json",
        "decay": memory_dir / "decay.json",
        "compacted": events_dir / "compacted_archive.json",
        "gitignore": memory_dir / ".gitignore"
    }


def ensure_memory_structure(root_dir: Optional[Path] = None) -> Dict[str, Path]:
    """Initialize memory directory layout with privacy isolation."""
    paths = get_memory_paths(root_dir)
    paths["memory"].mkdir(parents=True, exist_ok=True)
    paths["events"].mkdir(parents=True, exist_ok=True)

    # Privacy belt-and-suspenders: ignore everything inside .torusguard/memory/
    if not paths["gitignore"].exists():
        paths["gitignore"].write_text("*\n", encoding="utf-8")

    gitkeep = paths["events"] / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("", encoding="utf-8")

    if not paths["decay"].exists():
        decay_init = {
            "default_ttl_days": DEFAULT_TTL_DAYS,
            "decay_rate": DEFAULT_DECAY_RATE,
            "last_decay_run": None
        }
        paths["decay"].write_text(json.dumps(decay_init, indent=2), encoding="utf-8")

    if not paths["patterns"].exists():
        paths["patterns"].write_text("[]", encoding="utf-8")

    if not paths["profile"].exists():
        paths["profile"].write_text(json.dumps({
            "stack": [],
            "total_events": 0,
            "active_patterns_count": 0,
            "fix_rate_percentage": None,
            "top_vulnerabilities": [],
            "last_updated": datetime.datetime.utcnow().isoformat() + "Z"
        }, indent=2), encoding="utf-8")

    if not paths["context"].exists():
        initial_context = {
            "version": VERSION,
            "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
            "token_estimate": 0,
            "max_token_budget": DEFAULT_TOKEN_BUDGET,
            "project_profile": {
                "stack": [],
                "total_events": 0,
                "active_patterns_count": 0,
                "fix_rate_percentage": None,
                "top_vulnerabilities": []
            },
            "cards": []
        }
        paths["context"].write_text(json.dumps(initial_context, indent=2), encoding="utf-8")

    return paths


def estimate_tokens(obj: Any) -> int:
    """Rough conservative token estimation for JSON payloads (1 token ≈ 4 chars)."""
    serialized = json.dumps(obj, separators=(",", ":"))
    return max(1, len(serialized) // 4)


def record_event(
    event_type: str,
    data: Dict[str, Any],
    root_dir: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Append an individual raw event to .torusguard/memory/events/.
    Event types:
      - audit_finding
      - fix_applied
      - fix_verified
      - false_positive
      - pattern_learned
      - stack_changed
    """
    valid_types = {
        "audit_finding", "fix_applied", "fix_verified",
        "false_positive", "pattern_learned", "stack_changed"
    }
    if event_type not in valid_types:
        raise ValueError(f"Invalid event_type: {event_type}. Must be one of {valid_types}")

    paths = ensure_memory_structure(root_dir)
    now_utc = datetime.datetime.utcnow()
    timestamp_iso = now_utc.isoformat() + "Z"
    event_id = f"evt-{now_utc.strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}"

    # Sanitize file_path to be relative to project root
    raw_file = data.get("file_path")
    clean_file = None
    if raw_file:
        try:
            rel = Path(raw_file).resolve().relative_to(paths["root"].resolve())
            clean_file = str(rel).replace("\\", "/")
        except Exception:
            clean_file = str(raw_file).replace("\\", "/")

    event = {
        "event_id": event_id,
        "event_type": event_type,
        "timestamp": timestamp_iso,
        "version": VERSION,
        "rule_id": data.get("rule_id"),
        "file_path": clean_file,
        "line_number": data.get("line_number"),
        "severity": data.get("severity"),
        "confidence_score": data.get("confidence_score"),
        "code_hash": data.get("code_hash"),
        "fix_strategy": data.get("fix_strategy"),
        "verification_result": data.get("verification_result"),
        "suppression_reason": data.get("suppression_reason"),
        "metadata": data.get("metadata", {})
    }

    # Write event file with timestamp prefix for chronological directory ordering
    filename = f"{now_utc.strftime('%Y%m%d_%H%M%S')}_{event_id}.json"
    event_path = paths["events"] / filename
    event_path.write_text(json.dumps(event, indent=2), encoding="utf-8")

    return event


def load_all_events(root_dir: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Load all raw events from memory/events/ including compacted archive."""
    paths = ensure_memory_structure(root_dir)
    events: List[Dict[str, Any]] = []

    # 1. Load compacted archive if present
    if paths["compacted"].exists():
        try:
            with open(paths["compacted"], "r", encoding="utf-8") as f:
                archived = json.load(f)
                if isinstance(archived, list):
                    events.extend(archived)
        except Exception:
            pass

    # 2. Load individual event files
    if paths["events"].is_dir():
        for item in sorted(paths["events"].glob("*.json")):
            if item.name == "compacted_archive.json":
                continue
            try:
                with open(item, "r", encoding="utf-8") as f:
                    evt = json.load(f)
                    if isinstance(evt, dict) and "event_id" in evt:
                        events.append(evt)
            except Exception:
                continue

    # Deduplicate by event_id
    seen_ids = set()
    deduped = []
    for evt in events:
        eid = evt.get("event_id")
        if eid and eid not in seen_ids:
            seen_ids.add(eid)
            deduped.append(evt)

    # Sort chronologically
    deduped.sort(key=lambda x: x.get("timestamp", ""))
    return deduped


def distill_patterns(root_dir: Optional[Path] = None) -> List[Dict[str, Any]]:
    """
    Distill raw events into actionable, deduplicated security patterns.
    Pattern types:
      - recurring_fix: Repeated successful fixes for a rule
      - common_vulnerability: Vulnerabilities appearing frequently
      - false_positive_class: Suppressed rules/files
      - regression_watch: Rules/files that regressed or re-appeared
      - security_idiom: Project-specific established remediation practices
    """
    paths = ensure_memory_structure(root_dir)
    events = load_all_events(root_dir)
    patterns: List[Dict[str, Any]] = []

    if not events:
        paths["patterns"].write_text("[]", encoding="utf-8")
        compute_context_window(root_dir=root_dir)
        return patterns

    # Grouping indices
    rule_findings: Dict[str, List[Dict[str, Any]]] = {}
    rule_fixes: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    false_positives: Dict[str, List[Dict[str, Any]]] = {}
    regressions: Dict[str, List[Dict[str, Any]]] = {}

    for evt in events:
        etype = evt.get("event_type")
        rule_id = evt.get("rule_id")
        if not rule_id:
            continue

        if etype == "audit_finding":
            rule_findings.setdefault(rule_id, []).append(evt)
        elif etype == "fix_applied":
            strat = evt.get("fix_strategy") or "standard_remediation"
            rule_fixes.setdefault((rule_id, strat), []).append(evt)
        elif etype == "fix_verified":
            strat = evt.get("fix_strategy") or "standard_remediation"
            vres = evt.get("verification_result")
            if vres == "regressed":
                regressions.setdefault(rule_id, []).append(evt)
            else:
                rule_fixes.setdefault((rule_id, strat), []).append(evt)
        elif etype == "false_positive":
            false_positives.setdefault(rule_id, []).append(evt)

    pat_idx = 1

    # 1. Distill Recurring Fixes & Security Idioms
    for (rule_id, fix_strat), fix_evts in rule_fixes.items():
        occurrences = len(fix_evts)
        affected_files = sorted(list({e.get("file_path") for e in fix_evts if e.get("file_path")}))
        verified_count = sum(1 for e in fix_evts if e.get("verification_result") == "fixed")

        # Confidence amplification logic
        base_confidence = min(95, 50 + (occurrences * 10) + (verified_count * 10))
        # Multi-file bonus
        if len(affected_files) > 1:
            base_confidence = min(98, base_confidence + 5)

        pattern_type = "security_idiom" if occurrences >= 3 and verified_count >= 2 else "recurring_fix"
        timestamps = [e.get("timestamp") for e in fix_evts if e.get("timestamp")]
        first_seen = min(timestamps) if timestamps else datetime.datetime.utcnow().isoformat() + "Z"
        last_seen = max(timestamps) if timestamps else first_seen

        patterns.append({
            "pattern_id": f"PAT-{pat_idx:03d}",
            "rule_id": rule_id,
            "pattern_type": pattern_type,
            "description": f"Verified remediation strategy for {rule_id}: {fix_strat}",
            "fix_strategy": fix_strat,
            "confidence": base_confidence,
            "occurrences": occurrences,
            "affected_files": affected_files,
            "first_seen": first_seen,
            "last_seen": last_seen,
            "decay_checkpoint": last_seen,
            "source_events": [e.get("event_id") for e in fix_evts if e.get("event_id")]
        })
        pat_idx += 1

    # 2. Distill Common Vulnerabilities
    for rule_id, find_evts in rule_findings.items():
        occurrences = len(find_evts)
        if occurrences >= 2:
            affected_files = sorted(list({e.get("file_path") for e in find_evts if e.get("file_path")}))
            timestamps = [e.get("timestamp") for e in find_evts if e.get("timestamp")]
            first_seen = min(timestamps) if timestamps else datetime.datetime.utcnow().isoformat() + "Z"
            last_seen = max(timestamps) if timestamps else first_seen

            confidence = min(90, 55 + (occurrences * 5))
            patterns.append({
                "pattern_id": f"PAT-{pat_idx:03d}",
                "rule_id": rule_id,
                "pattern_type": "common_vulnerability",
                "description": f"Frequent vulnerability pattern detected across project for {rule_id}",
                "fix_strategy": None,
                "confidence": confidence,
                "occurrences": occurrences,
                "affected_files": affected_files,
                "first_seen": first_seen,
                "last_seen": last_seen,
                "decay_checkpoint": last_seen,
                "source_events": [e.get("event_id") for e in find_evts if e.get("event_id")]
            })
            pat_idx += 1

    # 3. Distill False Positive Classes
    for rule_id, fp_evts in false_positives.items():
        occurrences = len(fp_evts)
        affected_files = sorted(list({e.get("file_path") for e in fp_evts if e.get("file_path")}))
        reasons = [e.get("suppression_reason") for e in fp_evts if e.get("suppression_reason")]
        summary_reason = reasons[-1] if reasons else "Suppressed by team policy"
        timestamps = [e.get("timestamp") for e in fp_evts if e.get("timestamp")]
        first_seen = min(timestamps) if timestamps else datetime.datetime.utcnow().isoformat() + "Z"
        last_seen = max(timestamps) if timestamps else first_seen

        patterns.append({
            "pattern_id": f"PAT-{pat_idx:03d}",
            "rule_id": rule_id,
            "pattern_type": "false_positive_class",
            "description": f"Rule {rule_id} marked as false positive ({summary_reason})",
            "fix_strategy": None,
            "confidence": 90,
            "occurrences": occurrences,
            "affected_files": affected_files,
            "first_seen": first_seen,
            "last_seen": last_seen,
            "decay_checkpoint": last_seen,
            "source_events": [e.get("event_id") for e in fp_evts if e.get("event_id")]
        })
        pat_idx += 1

    # 4. Distill Regression Watch Entries
    for rule_id, reg_evts in regressions.items():
        occurrences = len(reg_evts)
        affected_files = sorted(list({e.get("file_path") for e in reg_evts if e.get("file_path")}))
        timestamps = [e.get("timestamp") for e in reg_evts if e.get("timestamp")]
        first_seen = min(timestamps) if timestamps else datetime.datetime.utcnow().isoformat() + "Z"
        last_seen = max(timestamps) if timestamps else first_seen

        patterns.append({
            "pattern_id": f"PAT-{pat_idx:03d}",
            "rule_id": rule_id,
            "pattern_type": "regression_watch",
            "description": f"High risk regression watch: {rule_id} re-occurred or failed verification",
            "fix_strategy": None,
            "confidence": 88,
            "occurrences": occurrences,
            "affected_files": affected_files,
            "first_seen": first_seen,
            "last_seen": last_seen,
            "decay_checkpoint": last_seen,
            "source_events": [e.get("event_id") for e in reg_evts if e.get("event_id")]
        })
        pat_idx += 1

    # Save patterns
    paths["patterns"].write_text(json.dumps(patterns, indent=2), encoding="utf-8")

    # Update profile and pre-computed context window
    get_project_profile(root_dir=root_dir)
    compute_context_window(root_dir=root_dir)

    return patterns


def decay_stale_entries(
    ttl_days: int = DEFAULT_TTL_DAYS,
    decay_rate: float = DEFAULT_DECAY_RATE,
    root_dir: Optional[Path] = None
) -> int:
    """
    Apply TTL decay to patterns not reconfirmed within ttl_days.
    Reduces confidence to prevent stale architectural advice.
    """
    paths = ensure_memory_structure(root_dir)
    now = datetime.datetime.utcnow()

    # Read config from decay.json if available
    try:
        if paths["decay"].exists():
            cfg = json.loads(paths["decay"].read_text(encoding="utf-8"))
            ttl_days = cfg.get("default_ttl_days", ttl_days)
            decay_rate = cfg.get("decay_rate", decay_rate)
    except Exception:
        pass

    if not paths["patterns"].exists():
        return 0

    try:
        patterns = json.loads(paths["patterns"].read_text(encoding="utf-8"))
    except Exception:
        return 0

    decayed_count = 0
    for pat in patterns:
        chk_str = pat.get("decay_checkpoint") or pat.get("last_seen")
        if not chk_str:
            continue
        try:
            # Parse ISO date string (strip Z if present)
            clean_ts = chk_str.rstrip("Z")
            last_dt = datetime.datetime.fromisoformat(clean_ts)
            days_elapsed = (now - last_dt).days

            if days_elapsed >= ttl_days:
                old_conf = pat.get("confidence", 50)
                reduction = max(5, int(old_conf * decay_rate))
                new_conf = max(10, old_conf - reduction)
                if new_conf != old_conf:
                    pat["confidence"] = new_conf
                    pat["decay_checkpoint"] = now.isoformat() + "Z"
                    decayed_count += 1
        except Exception:
            continue

    if decayed_count > 0:
        paths["patterns"].write_text(json.dumps(patterns, indent=2), encoding="utf-8")
        compute_context_window(root_dir=root_dir)

    # Record decay run in decay.json
    try:
        decay_cfg = {
            "default_ttl_days": ttl_days,
            "decay_rate": decay_rate,
            "last_decay_run": now.isoformat() + "Z",
            "last_decayed_count": decayed_count
        }
        paths["decay"].write_text(json.dumps(decay_cfg, indent=2), encoding="utf-8")
    except Exception:
        pass

    return decayed_count


def get_project_profile(root_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Compute and update the project's security DNA profile."""
    paths = ensure_memory_structure(root_dir)
    events = load_all_events(root_dir)

    # Detect stack from torusguard.json if available
    detected_stack: List[str] = []
    config_file = paths["torusguard"] / "config" / "torusguard.json"
    if config_file.exists():
        try:
            cfg = json.loads(config_file.read_text(encoding="utf-8"))
            stk = cfg.get("detected_stack", {})
            for k in ("language", "framework", "data_layer"):
                v = stk.get(k)
                if v and v not in ("None", "Unknown"):
                    detected_stack.append(v)
        except Exception:
            pass

    # Count statistics
    findings_count = 0
    fixes_count = 0
    verified_fixed_count = 0
    vuln_counter: Dict[str, int] = {}

    for evt in events:
        etype = evt.get("event_type")
        rid = evt.get("rule_id")
        if etype == "audit_finding":
            findings_count += 1
            if rid:
                vuln_counter[rid] = vuln_counter.get(rid, 0) + 1
        elif etype == "fix_applied":
            fixes_count += 1
        elif etype == "fix_verified":
            if evt.get("verification_result") == "fixed":
                verified_fixed_count += 1

    fix_rate = None
    if findings_count > 0:
        fix_rate = round((verified_fixed_count / findings_count) * 100, 1)

    top_vulns = [item[0] for item in sorted(vuln_counter.items(), key=lambda x: x[1], reverse=True)[:5]]

    # Count active patterns
    active_patterns_count = 0
    if paths["patterns"].exists():
        try:
            pats = json.loads(paths["patterns"].read_text(encoding="utf-8"))
            active_patterns_count = len(pats)
        except Exception:
            pass

    profile = {
        "stack": detected_stack,
        "total_events": len(events),
        "active_patterns_count": active_patterns_count,
        "findings_count": findings_count,
        "fixes_applied_count": fixes_count,
        "fixes_verified_count": verified_fixed_count,
        "fix_rate_percentage": fix_rate,
        "top_vulnerabilities": top_vulns,
        "last_updated": datetime.datetime.utcnow().isoformat() + "Z"
    }

    paths["profile"].write_text(json.dumps(profile, indent=2), encoding="utf-8")
    return profile


def compute_context_window(
    max_tokens: int = DEFAULT_TOKEN_BUDGET,
    root_dir: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Build the pre-computed, token-budgeted context window as structured JSON cards.
    Guarantees strict token enforcement <= max_tokens.
    """
    paths = ensure_memory_structure(root_dir)
    profile = get_project_profile(root_dir=root_dir)

    patterns: List[Dict[str, Any]] = []
    if paths["patterns"].exists():
        try:
            patterns = json.loads(paths["patterns"].read_text(encoding="utf-8"))
        except Exception:
            patterns = []

    # Sort patterns by priority: regressions (95) -> idioms (90) -> recurring fixes (85) -> FP (80) -> common vulns (70)
    type_priority = {
        "regression_watch": 95,
        "security_idiom": 90,
        "recurring_fix": 85,
        "false_positive_class": 80,
        "common_vulnerability": 70
    }

    # Generate Candidate Cards
    cards: List[Dict[str, Any]] = []
    card_idx = 1

    # 1. Project Profile Card (Priority: 100)
    cards.append({
        "card_id": f"CARD-{card_idx:03d}",
        "card_type": "profile",
        "priority": 100,
        "title": "Project Security Posture & DNA",
        "summary": f"Stack: {', '.join(profile.get('stack') or ['Generic'])}; Total Events: {profile.get('total_events', 0)}; Fix Rate: {profile.get('fix_rate_percentage')}%",
        "card_data": {
            "stack": profile.get("stack", []),
            "total_events": profile.get("total_events", 0),
            "fix_rate_percentage": profile.get("fix_rate_percentage"),
            "top_vulnerabilities": profile.get("top_vulnerabilities", [])
        }
    })
    card_idx += 1

    # Sort patterns by type priority then confidence then occurrences
    sorted_patterns = sorted(
        patterns,
        key=lambda p: (
            type_priority.get(p.get("pattern_type", ""), 50),
            p.get("confidence", 0),
            p.get("occurrences", 0)
        ),
        reverse=True
    )

    for pat in sorted_patterns:
        ptype = pat.get("pattern_type", "pattern")
        card_type = "pattern"
        if ptype == "regression_watch":
            card_type = "regression_watch"
        elif ptype == "false_positive_class":
            card_type = "false_positive"
        elif ptype == "security_idiom":
            card_type = "fix_idiom"

        cards.append({
            "card_id": f"CARD-{card_idx:03d}",
            "card_type": card_type,
            "priority": type_priority.get(ptype, 60),
            "title": f"[{pat.get('rule_id')}] {pat.get('pattern_type')}: {pat.get('description', '')[:60]}",
            "summary": pat.get("description", ""),
            "card_data": {
                "rule_id": pat.get("rule_id"),
                "pattern_type": pat.get("pattern_type"),
                "fix_strategy": pat.get("fix_strategy"),
                "confidence": pat.get("confidence"),
                "occurrences": pat.get("occurrences"),
                "affected_files": pat.get("affected_files", [])[:5]
            }
        })
        card_idx += 1

    # Build Context Window Payload
    context = {
        "version": VERSION,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "token_estimate": 0,
        "max_token_budget": max_tokens,
        "project_profile": {
            "stack": profile.get("stack", []),
            "total_events": profile.get("total_events", 0),
            "active_patterns_count": profile.get("active_patterns_count", 0),
            "fix_rate_percentage": profile.get("fix_rate_percentage"),
            "top_vulnerabilities": profile.get("top_vulnerabilities", [])
        },
        "cards": cards
    }

    # Token budget enforcement: Drop lowest-priority cards until within limit
    # Always keep at least the profile card (cards[0])
    while len(context["cards"]) > 1 and estimate_tokens(context) > max_tokens:
        context["cards"].pop()

    context["token_estimate"] = estimate_tokens(context)

    # Persist context.json
    paths["context"].write_text(json.dumps(context, indent=2), encoding="utf-8")
    return context


def get_context(root_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Retrieve the current pre-computed context window."""
    paths = ensure_memory_structure(root_dir)
    if paths["context"].exists():
        try:
            return json.loads(paths["context"].read_text(encoding="utf-8"))
        except Exception:
            pass

    return compute_context_window(root_dir=root_dir)


def record_false_positive(
    rule_id: str,
    file_path: Optional[str] = None,
    reason: str = "False positive verified by user",
    root_dir: Optional[Path] = None
) -> Dict[str, Any]:
    """Record a false positive suppression and update patterns."""
    evt = record_event(
        "false_positive",
        {
            "rule_id": rule_id,
            "file_path": file_path,
            "suppression_reason": reason
        },
        root_dir=root_dir
    )
    distill_patterns(root_dir=root_dir)
    return evt


def export_memory(target_path: str, root_dir: Optional[Path] = None) -> Dict[str, Any]:
    """
    Export memory to an external file for team sharing.
    Per user choice: retain code hashes for high-fidelity matching, but sanitize absolute paths.
    """
    paths = ensure_memory_structure(root_dir)
    events = load_all_events(root_dir)
    profile = get_project_profile(root_dir=root_dir)

    patterns = []
    if paths["patterns"].exists():
        try:
            patterns = json.loads(paths["patterns"].read_text(encoding="utf-8"))
        except Exception:
            pass

    decay_cfg = {}
    if paths["decay"].exists():
        try:
            decay_cfg = json.loads(paths["decay"].read_text(encoding="utf-8"))
        except Exception:
            pass

    export_payload = {
        "format": "torusguard-memory-bundle",
        "schema_version": "1.0.0",
        "exported_at": datetime.datetime.utcnow().isoformat() + "Z",
        "project_profile": profile,
        "decay_config": decay_cfg,
        "patterns": patterns,
        "events": events
    }

    out_file = Path(target_path).resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(export_payload, indent=2), encoding="utf-8")

    return {
        "target_path": str(out_file),
        "exported_events_count": len(events),
        "exported_patterns_count": len(patterns)
    }


def import_memory(source_path: str, merge: bool = True, root_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Import and optionally merge external memory events and patterns."""
    paths = ensure_memory_structure(root_dir)
    src = Path(source_path).resolve()
    if not src.is_file():
        raise FileNotFoundError(f"Export file not found: {source_path}")

    with open(src, "r", encoding="utf-8") as f:
        payload = json.load(f)

    imported_events = payload.get("events", [])
    if not isinstance(imported_events, list):
        raise ValueError("Malformed import payload: 'events' must be a list")

    count = 0
    for evt in imported_events:
        eid = evt.get("event_id")
        if not eid:
            continue
        filename = f"imported_{eid}.json"
        dest = paths["events"] / filename
        if not dest.exists() or not merge:
            dest.write_text(json.dumps(evt, indent=2), encoding="utf-8")
            count += 1

    distill_patterns(root_dir=root_dir)

    return {
        "source_path": str(src),
        "imported_events_count": count,
        "active_patterns_count": len(json.loads(paths["patterns"].read_text(encoding="utf-8")))
    }


def compact_events(older_than_days: int = 30, root_dir: Optional[Path] = None) -> int:
    """
    Compact loose event JSON files older than older_than_days into compacted_archive.json.
    Prevents filesystem inode saturation while preserving full history.
    """
    paths = ensure_memory_structure(root_dir)
    cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=older_than_days)

    archived: List[Dict[str, Any]] = []
    if paths["compacted"].exists():
        try:
            with open(paths["compacted"], "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    archived = data
        except Exception:
            archived = []

    archived_ids = {e.get("event_id") for e in archived if e.get("event_id")}
    compacted_count = 0

    for item in sorted(paths["events"].glob("*.json")):
        if item.name == "compacted_archive.json":
            continue
        try:
            with open(item, "r", encoding="utf-8") as f:
                evt = json.load(f)
            ts_str = evt.get("timestamp", "").rstrip("Z")
            evt_dt = datetime.datetime.fromisoformat(ts_str) if ts_str else None
            if evt_dt and evt_dt < cutoff:
                eid = evt.get("event_id")
                if eid and eid not in archived_ids:
                    archived.append(evt)
                    archived_ids.add(eid)
                item.unlink(missing_ok=True)
                compacted_count += 1
        except Exception:
            continue

    if compacted_count > 0 or not paths["compacted"].exists():
        paths["compacted"].write_text(json.dumps(archived, indent=2), encoding="utf-8")

    return compacted_count


# ─── Command Line Interface ──────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="TorusGuard Security Memory Engine")
    parser.add_argument("--action", required=True, choices=[
        "record", "distill", "context", "profile", "decay", "fp", "export", "import", "compact", "status"
    ], help="Action to perform")
    parser.add_argument("--root", help="Project root directory override")
    parser.add_argument("--type", help="Event type (audit_finding, fix_applied, etc.)")
    parser.add_argument("--rule-id", help="TorusGuard rule ID (e.g., TG-DB-004)")
    parser.add_argument("--file", help="File path")
    parser.add_argument("--line", type=int, help="Line number")
    parser.add_argument("--severity", choices=["critical", "high", "medium", "low", "info"])
    parser.add_argument("--score", type=int, help="Confidence score (0-100)")
    parser.add_argument("--strategy", help="Fix strategy description")
    parser.add_argument("--result", choices=["fixed", "regressed", "partial", "not_tested"])
    parser.add_argument("--reason", help="Suppression reason for false positive")
    parser.add_argument("--target", help="Export target path")
    parser.add_argument("--source", help="Import source path")
    parser.add_argument("--ttl", type=int, default=DEFAULT_TTL_DAYS, help="Decay TTL in days")
    parser.add_argument("--older-than", type=int, default=30, help="Compaction age in days")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()
    root = Path(args.root).resolve() if args.root else None

    if args.action == "record":
        if not args.type:
            print("Error: --type is required for record action", file=sys.stderr)
            sys.exit(1)
        data = {
            "rule_id": args.rule_id,
            "file_path": args.file,
            "line_number": args.line,
            "severity": args.severity,
            "confidence_score": args.score,
            "fix_strategy": args.strategy,
            "verification_result": args.result,
            "suppression_reason": args.reason
        }
        evt = record_event(args.type, data, root_dir=root)
        distill_patterns(root_dir=root)
        print(json.dumps(evt, indent=2) if args.json else f"Recorded event: {evt['event_id']}")

    elif args.action == "distill":
        pats = distill_patterns(root_dir=root)
        if args.json:
            print(json.dumps(pats, indent=2))
        else:
            print(f"Distilled {len(pats)} active patterns.")

    elif args.action == "context":
        ctx = get_context(root_dir=root)
        print(json.dumps(ctx, indent=2))

    elif args.action == "profile":
        prof = get_project_profile(root_dir=root)
        print(json.dumps(prof, indent=2))

    elif args.action == "decay":
        decayed = decay_stale_entries(ttl_days=args.ttl, root_dir=root)
        print(f"Decayed {decayed} patterns older than {args.ttl} days.")

    elif args.action == "fp":
        if not args.rule_id:
            print("Error: --rule-id is required for fp action", file=sys.stderr)
            sys.exit(1)
        evt = record_false_positive(args.rule_id, file_path=args.file, reason=args.reason or "False positive", root_dir=root)
        print(f"Suppressed false positive for {args.rule_id}")

    elif args.action == "export":
        if not args.target:
            print("Error: --target is required for export action", file=sys.stderr)
            sys.exit(1)
        res = export_memory(args.target, root_dir=root)
        print(json.dumps(res, indent=2) if args.json else f"Exported {res['exported_events_count']} events to {res['target_path']}")

    elif args.action == "import":
        if not args.source:
            print("Error: --source is required for import action", file=sys.stderr)
            sys.exit(1)
        res = import_memory(args.source, root_dir=root)
        print(json.dumps(res, indent=2) if args.json else f"Imported {res['imported_events_count']} events from {res['source_path']}")

    elif args.action == "compact":
        n = compact_events(older_than_days=args.older_than, root_dir=root)
        print(f"Compacted {n} events older than {args.older_than} days.")

    elif args.action == "status":
        prof = get_project_profile(root_dir=root)
        ctx = get_context(root_dir=root)
        print(f"Memory Status (v{VERSION}):")
        print(f"  Events Recorded:   {prof.get('total_events', 0)}")
        print(f"  Patterns Active:   {prof.get('active_patterns_count', 0)}")
        print(f"  Context Estimate:  {ctx.get('token_estimate', 0)} / {ctx.get('max_token_budget', DEFAULT_TOKEN_BUDGET)} tokens")
        print(f"  Fix Velocity Rate: {prof.get('fix_rate_percentage')}%")


if __name__ == "__main__":
    main()
