#!/usr/bin/env python3
"""
TorusGuard Finding Confidence Scorer (v1.0.0)
Evaluates finding confidence against the objective 0–100 scoring model,
augmented by persistent memory patterns and false-positive suppression.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Tuple, Optional


def compute_memory_boost(
    rule_id: str,
    file_path: Optional[str] = None,
    root_dir: Optional[Path] = None
) -> int:
    """
    Query .torusguard/memory/patterns.json to calculate memory confidence modifier:
    - False positive class: -30 (heavily suppressed)
    - Regression watch: +15 (high alert / known recurrence)
    - Recurring fix / Common vulnerability: +10
    - Security idiom: +5
    - Multi-file pattern match bonus: +5
    """
    if not rule_id:
        return 0

    base = Path(root_dir or Path.cwd()).resolve()
    # Search for .torusguard
    torusguard_dir = base / ".torusguard"
    if not torusguard_dir.exists():
        for parent in base.parents:
            if (parent / ".torusguard").exists():
                torusguard_dir = parent / ".torusguard"
                break

    patterns_file = torusguard_dir / "memory" / "patterns.json"
    if not patterns_file.exists():
        return 0

    try:
        with open(patterns_file, "r", encoding="utf-8") as f:
            patterns = json.load(f)
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return 0

    boost = 0
    matched_file = False
    matched_dir = False
    target_path = Path(file_path) if file_path else None

    for pat in patterns:
        if pat.get("rule_id") == rule_id:
            ptype = pat.get("pattern_type")
            if ptype == "false_positive_class":
                boost -= 30
            elif ptype == "regression_watch":
                boost += 15
            elif ptype in ("recurring_fix", "common_vulnerability"):
                boost += 10
            elif ptype == "security_idiom":
                boost += 5

            # File-specific and directory-level correlation bonus
            affected = pat.get("affected_files", [])
            if file_path and file_path in affected:
                matched_file = True
            elif target_path and any(target_path.parent == Path(af).parent for af in affected if af):
                matched_dir = True

    if matched_file and boost > 0:
        boost += 5
    elif matched_file and boost < 0:
        boost -= 10
    elif matched_dir and boost > 0:
        boost += 2
    elif matched_dir and boost < 0:
        boost -= 4

    return boost


def compute_confidence_score(
    evidence_quality: int = 35,
    reproduction_success: int = 0,
    independent_confirmations: int = 5,
    environmental_clarity: int = 15,
    manual_review_status: int = 0,
    memory_boost: int = 0,
    rule_id: Optional[str] = None,
    file_path: Optional[str] = None,
    root_dir: Optional[Path] = None
) -> Tuple[int, str, Dict[str, Any]]:
    """
    Computes total score and assigns confidence band.
    Max points:
    - evidence_quality: 35
    - reproduction_success: 25
    - independent_confirmations: 15
    - environmental_clarity: 15
    - manual_review_status: 10
    - memory_boost: -30 to +20 (modifier from persistent memory)
    Total is clamped to [0, 100].
    """
    eq = min(max(evidence_quality, 0), 35)
    rs = min(max(reproduction_success, 0), 25)
    ic = min(max(independent_confirmations, 0), 15)
    ec = min(max(environmental_clarity, 0), 15)
    mr = min(max(manual_review_status, 0), 10)

    # Auto-calculate memory boost if rule_id provided and memory_boost == 0
    eff_mem_boost = memory_boost
    if rule_id and eff_mem_boost == 0:
        eff_mem_boost = compute_memory_boost(rule_id, file_path=file_path, root_dir=root_dir)

    raw_total = eq + rs + ic + ec + mr + eff_mem_boost
    total = min(max(raw_total, 0), 100)

    if total >= 90:
        band = "Confirmed"
    elif total >= 70:
        band = "High Confidence"
    elif total >= 50:
        band = "Medium Confidence"
    else:
        band = "Needs Review"

    factors = {
        "evidence_quality": eq,
        "reproduction_success": rs,
        "independent_confirmations": ic,
        "environmental_clarity": ec,
        "manual_review_status": mr,
        "memory_boost": eff_mem_boost,
        "total_score": total,
        "classification_band": band
    }
    return total, band, factors


def main():
    parser = argparse.ArgumentParser(description="TorusGuard Confidence Scorer")
    parser.add_argument("--eq", type=int, default=35, help="Evidence quality score (0-35)")
    parser.add_argument("--rs", type=int, default=0, help="Reproduction success score (0-25)")
    parser.add_argument("--ic", type=int, default=5, help="Independent confirmations score (0-15)")
    parser.add_argument("--ec", type=int, default=15, help="Environmental clarity score (0-15)")
    parser.add_argument("--mr", type=int, default=0, help="Manual review status score (0-10)")
    parser.add_argument("--memory-boost", type=int, default=0, help="Memory boost score (-30 to +20)")
    parser.add_argument("--rule-id", type=str, help="TorusGuard rule ID for memory pattern matching")
    parser.add_argument("--file", type=str, help="File path for correlation matching")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    total, band, factors = compute_confidence_score(
        evidence_quality=args.eq,
        reproduction_success=args.rs,
        independent_confirmations=args.ic,
        environmental_clarity=args.ec,
        manual_review_status=args.mr,
        memory_boost=args.memory_boost,
        rule_id=args.rule_id,
        file_path=args.file
    )

    if args.json:
        print(json.dumps(factors, indent=2))
    else:
        print(f"Total Confidence Score: {total}/100")
        print(f"Classification Band: {band}")
        print("Factor Breakdown:")
        for k, v in factors.items():
            if k not in ("total_score", "classification_band"):
                print(f"  - {k}: {v}")


if __name__ == "__main__":
    main()
