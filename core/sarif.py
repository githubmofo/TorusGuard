"""
TorusGuard v6 SARIF v2.1.0 Exporter
Emits standard SARIF-compatible JSON reports for CI/CD, GitHub Security Code Scanning, and SIEM tool integration.
"""

import json
from typing import List, Dict, Any, Optional
from pathlib import Path


class SarifExporter:
    """
    Transforms TorusGuard findings and clusters into standard SARIF v2.1.0 format.
    """

    SARIF_VERSION = "2.1.0"
    SARIF_SCHEMA = "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json"

    @classmethod
    def generate_sarif(
        cls,
        findings: List[Dict[str, Any]],
        clusters: Optional[List[Dict[str, Any]]] = None,
        tool_version: str = "6.0.0",
    ) -> Dict[str, Any]:
        """
        Builds a complete SARIF log dict.
        """
        rules_map: Dict[str, Dict[str, Any]] = {}
        results: List[Dict[str, Any]] = []

        for f in findings:
            rule_id = f.get("rule_id", "TG-GENERIC")
            finding_id = f.get("finding_id", "")
            title = f.get("title", rule_id)
            severity = f.get("severity", "High")
            confidence_score = f.get("confidence_score", 80)
            confidence_band = f.get("confidence_band", "High Confidence")
            cluster_id = f.get("cluster_id", "")

            target = f.get("target", {})
            file_path = target.get("file_path", "unknown").replace("\\", "/")
            start_line = max(1, target.get("line_start", 1))
            end_line = max(start_line, target.get("line_end", start_line))

            evidence_snippet = f.get("evidence", {}).get("code_snippet", "")
            fingerprint = f.get("fingerprint_id", finding_id)

            # Map Severity to SARIF level
            sarif_level = "warning"
            if severity in ["Critical", "High"]:
                sarif_level = "error"
            elif severity in ["Low", "Informational"]:
                sarif_level = "note"

            # Register rule if not already present
            if rule_id not in rules_map:
                rules_map[rule_id] = {
                    "id": rule_id,
                    "name": rule_id.replace("-", "_"),
                    "shortDescription": {"text": title},
                    "fullDescription": {
                        "text": f"TorusGuard Rule {rule_id}: {title}"
                    },
                    "defaultConfiguration": {"level": sarif_level},
                    "help": {
                        "text": f"Read documentation for {rule_id} at https://github.com/githubmofo/TorusGuard"
                    },
                    "properties": {
                        "category": f.get("category", "security"),
                    }
                }

            # Construct Result Object
            result_obj: Dict[str, Any] = {
                "ruleId": rule_id,
                "ruleIndex": list(rules_map.keys()).index(rule_id),
                "level": sarif_level,
                "message": {
                    "text": f"[{rule_id}] {title} (Confidence: {confidence_score}/100 - {confidence_band})"
                },
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {
                                "uri": file_path,
                                "uriBaseId": "%SRCROOT%"
                            },
                            "region": {
                                "startLine": start_line,
                                "endLine": end_line,
                                "snippet": {
                                    "text": evidence_snippet
                                }
                            }
                        }
                    }
                ],
                "fingerprints": {
                    "torusguard/v6/stable_identity": fingerprint
                },
                "properties": {
                    "finding_id": finding_id,
                    "confidence_score": confidence_score,
                    "confidence_band": confidence_band,
                    "cluster_id": cluster_id,
                    "recheck_status": f.get("recheck_status", "Unrechecked")
                }
            }
            results.append(result_obj)

        sarif_payload = {
            "$schema": cls.SARIF_SCHEMA,
            "version": cls.SARIF_VERSION,
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "TorusGuard",
                            "semanticVersion": tool_version,
                            "informationUri": "https://github.com/githubmofo/TorusGuard",
                            "rules": list(rules_map.values()),
                        }
                    },
                    "results": results
                }
            ]
        }

        return sarif_payload
