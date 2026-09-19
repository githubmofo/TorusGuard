#!/usr/bin/env python3
"""
TorusGuard Runtime Safety Gate Evaluator
Evaluates prospective HTTP/browser validation probes against non-destruction policies.
"""

import sys
import json
import argparse
from typing import Dict, Any, Tuple

def evaluate_safety_gate(method: str, path: str, body: str = "") -> Tuple[str, str]:
    """
    Returns (decision, rationale)
    Decisions:
    - Auto-Allowed
    - Approval Required
    - Manual Only (Blocked)
    """
    method_upper = method.upper()

    # Block destructive verbs
    if method_upper in ("DELETE", "DROP"):
        return "Manual Only", f"Method '{method_upper}' is destructive and strictly blocked from automated runtime validation."

    # Block sensitive administrative paths
    destructive_keywords = ["/admin/delete", "/shutdown", "/drop-database", "/purge", "/reset-system"]
    for kw in destructive_keywords:
        if kw in path.lower():
            return "Manual Only", f"Path '{path}' targets destructive administrative endpoint '{kw}'."

    # Safe read methods
    if method_upper in ("GET", "HEAD", "OPTIONS"):
        return "Auto-Allowed", f"Read-only method '{method_upper}' with non-destructive path."

    # State-changing methods (POST, PUT, PATCH)
    if method_upper in ("POST", "PUT", "PATCH"):
        # Check if safe canary marker exists
        if "tg-canary" in body.lower() or "torusguard" in body.lower():
            return "Approval Required", f"State-changing method '{method_upper}' contains benign TorusGuard test marker; requires user approval."
        else:
            return "Approval Required", f"State-changing method '{method_upper}' requires operator approval before execution."

    return "Approval Required", f"Unknown probe profile for {method_upper} {path}."


def main():
    parser = argparse.ArgumentParser(description="TorusGuard Safety Gate Evaluator")
    parser.add_argument("--method", "-m", default="GET", help="HTTP Method")
    parser.add_argument("--path", "-p", default="/api/test", help="Endpoint path")
    parser.add_argument("--body", "-b", default="", help="Request payload body")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    decision, rationale = evaluate_safety_gate(args.method, args.path, args.body)

    if args.json:
        print(json.dumps({"decision": decision, "rationale": rationale}, indent=2))
    else:
        print(f"Safety Decision: {decision}")
        print(f"Rationale: {rationale}")

if __name__ == "__main__":
    main()
