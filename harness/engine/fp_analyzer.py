"""
TorusGuard False Positive & False Negative Analyzer (v0.5.2)
Diagnoses rule discrepancies, weak evidence signals, and generates follow-up remediation recommendations.
"""

from typing import List, Dict, Any
from .models import ComparisonResult, ValidationOutcome


class FalsePositiveAnalyzer:
    """
    Analyzes differential outcome mismatches and provides root-cause diagnostics for rule refinements.
    """

    @staticmethod
    def analyze_results(results: List[ComparisonResult]) -> List[Dict[str, Any]]:
        diagnostics: List[Dict[str, Any]] = []

        for r in results:
            if r.outcome == ValidationOutcome.FALSE_POSITIVE:
                diagnostics.append({
                    "fixture_id": r.fixture_id,
                    "rule_id": r.rule_id,
                    "category": "False Positive",
                    "severity": "High",
                    "root_cause": f"Rule {r.rule_id} triggered on safe pattern in {r.framework} fixture.",
                    "recommended_action": f"Refine AST/regex rule definition in rules/ to account for safe idiom in {r.framework}.",
                })
            elif r.outcome == ValidationOutcome.FALSE_NEGATIVE:
                diagnostics.append({
                    "fixture_id": r.fixture_id,
                    "rule_id": r.rule_id,
                    "category": "False Negative",
                    "severity": "Critical",
                    "root_cause": f"Rule {r.rule_id} failed to trigger on confirmed vulnerable pattern in {r.framework}.",
                    "recommended_action": f"Expand rule trigger patterns in {r.rule_id} to capture the unmitigated syntax variant.",
                })
            elif r.outcome == ValidationOutcome.NEEDS_REVIEW:
                diagnostics.append({
                    "fixture_id": r.fixture_id,
                    "rule_id": r.rule_id,
                    "category": "Ambiguous Evidence",
                    "severity": "Medium",
                    "root_cause": "Evidence is delegated out-of-band (service layer or proxy).",
                    "recommended_action": "Ensure prompt explicitly requests developer verification of out-of-band architecture.",
                })

        return diagnostics
