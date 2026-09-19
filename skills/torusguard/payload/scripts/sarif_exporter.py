#!/usr/bin/env python3
"""
TorusGuard OASIS SARIF v2.1.0 Exporter
Converts normalized TorusGuard findings into standard SARIF v2.1.0 format with
GitHub Code Scanning multi-analysis category separation and partialFingerprints deduplication.
"""

import sys
import json
import hashlib
import argparse
from pathlib import Path
from typing import List, Dict, Any

def generate_sarif(findings: List[Dict[str, Any]], run_id: str = "default", category: str = "torusguard/static") -> Dict[str, Any]:
    rules_map: Dict[str, Dict[str, Any]] = {}
    results: List[Dict[str, Any]] = []

    for f in findings:
        rule_id = f.get("rule_id", "TG-GEN-001")
        if rule_id not in rules_map:
            rules_map[rule_id] = {
                "id": rule_id,
                "name": f.get("title", rule_id),
                "shortDescription": {"text": f.get("title", rule_id)},
                "fullDescription": {"text": f.get("description", f.get("title", rule_id))},
                "defaultConfiguration": {
                    "level": "error" if f.get("severity") in ("Critical", "High") else "warning"
                },
                "properties": {
                    "tags": ["security", "torusguard", f.get("category", "general")]
                }
            }

        target = f.get("target", {})
        file_path = target.get("file_path", "unknown")
        line = target.get("start_line", 1)

        # Generate deduplication fingerprint
        seed = f"{rule_id}:{file_path}:{line}"
        line_hash = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]

        result: Dict[str, Any] = {
            "ruleId": rule_id,
            "message": {"text": f.get("title", "TorusGuard Security Finding")},
            "level": "error" if f.get("severity") in ("Critical", "High") else "warning",
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": file_path,
                            "uriBaseId": "%SRCROOT%"
                        },
                        "region": {
                            "startLine": line,
                            "startColumn": 1
                        }
                    }
                }
            ],
            "partialFingerprints": {
                "primaryLocationLineHash": line_hash
            },
            "properties": {
                "confidence": f.get("confidence", 70),
                "status": f.get("status", "Confirmed"),
                "finding_id": f.get("finding_id", "TG-FIND-UNKNOWN")
            }
        }
        results.append(result)

    sarif = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "TorusGuard",
                        "semanticVersion": "1.3.6",
                        "informationUri": "https://github.com/githubmofo/TorusGuard",
                        "rules": list(rules_map.values())
                    }
                },
                "automationDetails": {
                    "id": f"{category}/{run_id}"
                },
                "results": results
            }
        ]
    }
    return sarif


def main():
    parser = argparse.ArgumentParser(description="TorusGuard SARIF v2.1.0 Exporter")
    parser.add_argument("--input", "-i", help="Path to findings JSON file")
    parser.add_argument("--output", "-o", help="Output path for sarif.json")
    parser.add_argument("--root", "-r", help="Project root override")
    parser.add_argument("--run-id", default=None, help="Unique execution Run ID")
    parser.add_argument("--stdout", action="store_true", help="Print SARIF JSON to stdout")
    args = parser.parse_args()

    root = Path(args.root).resolve() if args.root else Path.cwd().resolve()
    findings = []
    run_id = args.run_id or "run-default"

    if args.input:
        in_path = Path(args.input)
        if not in_path.is_absolute():
            in_path = (root / in_path).resolve()
        if in_path.is_file():
            with open(in_path, "r", encoding="utf-8") as f:
                findings = json.load(f)
    else:
        # Auto-discover latest audit run findings
        runs_dir = root / ".torusguard" / "runs"
        if runs_dir.is_dir():
            run_folders = sorted(
                [d for d in runs_dir.iterdir() if d.is_dir() and (d / "findings.json").is_file()],
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )
            if run_folders:
                latest_run = run_folders[0]
                run_id = args.run_id or latest_run.name
                findings_file = latest_run / "findings.json"
                try:
                    with open(findings_file, "r", encoding="utf-8") as f:
                        findings = json.load(f)
                except Exception:
                    findings = []

    sarif = generate_sarif(findings, run_id=run_id)

    if args.output:
        out_path = Path(args.output)
        if not out_path.is_absolute():
            out_path = (root / out_path).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(sarif, f, indent=2)
        print(f"[SUCCESS] SARIF log written to: {out_path}")
    elif args.stdout:
        print(json.dumps(sarif, indent=2))
    else:
        # Default to writing in .torusguard/runs/results-latest.sarif
        default_sarif = root / ".torusguard" / "runs" / "results-latest.sarif"
        default_sarif.parent.mkdir(parents=True, exist_ok=True)
        with open(default_sarif, "w", encoding="utf-8") as f:
            json.dump(sarif, f, indent=2)
        print(f"[SUCCESS] SARIF log written to: {default_sarif}")


if __name__ == "__main__":
    main()
