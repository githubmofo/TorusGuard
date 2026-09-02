#!/usr/bin/env python3
"""
TorusGuard 5-Factor Finding Confidence Scorer
Evaluates finding confidence against the objective 0–100 scoring model.
"""

import sys
import json
import argparse
from typing import Dict, Any, Tuple

def compute_confidence_score(
    evidence_quality: int = 35,
    reproduction_success: int = 0,
    independent_confirmations: int = 5,
    environmental_clarity: int = 15,
    manual_review_status: int = 0
) -> Tuple[int, str, Dict[str, int]]:
    """
    Computes total score and assigns confidence band.
    Max points:
    - evidence_quality: 35
    - reproduction_success: 25
    - independent_confirmations: 15
    - environmental_clarity: 15
    - manual_review_status: 10
    """
    eq = min(max(evidence_quality, 0), 35)
    rs = min(max(reproduction_success, 0), 25)
    ic = min(max(independent_confirmations, 0), 15)
    ec = min(max(environmental_clarity, 0), 15)
    mr = min(max(manual_review_status, 0), 10)

    total = eq + rs + ic + ec + mr

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
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    total, band, factors = compute_confidence_score(
        evidence_quality=args.eq,
        reproduction_success=args.rs,
        independent_confirmations=args.ic,
        environmental_clarity=args.ec,
        manual_review_status=args.mr
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
