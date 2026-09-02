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
                        "semanticVersion": "0.8.0",
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
    parser.add_argument("--run-id", default="run-default", help="Unique execution Run ID")
    args = parser.parse_args()

    findings = []
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            findings = json.load(f)

    sarif = generate_sarif(findings, run_id=args.run_id)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(sarif, f, indent=2)
        print(f"SARIF log written to: {args.output}")
    else:
        print(json.dumps(sarif, indent=2))

if __name__ == "__main__":
    main()
