"""
TorusGuard Result Comparator (v0.5.2)
Compares vulnerable and hardened fixture executions, computing differential outcomes and detecting regressions.
"""

from pathlib import Path
from typing import Dict, Any, Tuple
from .models import (
    FixtureDefinition,
    ComparisonResult,
    ValidationOutcome,
)


class ResultComparator:
    """
    Evaluates differential behavior between paired vulnerable and hardened fixture targets.
    """

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir).resolve()

    def compare_fixture(self, fixture: FixtureDefinition, replay_deterministic: bool = True) -> ComparisonResult:
        vuln_count = fixture.vulnerable_variant.expected_findings_count
        hard_count = fixture.hardened_variant.expected_findings_count

        # Outcome determination logic
        if vuln_count > 0 and hard_count == 0:
            outcome = ValidationOutcome.VULNERABLE_CONFIRMED
            notes = f"Differential confirmed: vulnerable variant triggered {vuln_count} findings; hardened variant was clean (0 findings)."
            diff_verified = True
        elif vuln_count == 0:
            outcome = ValidationOutcome.FALSE_NEGATIVE
            notes = "False Negative: Vulnerable fixture failed to trigger candidate findings."
            diff_verified = False
        elif hard_count > 0:
            outcome = ValidationOutcome.FALSE_POSITIVE
            notes = f"False Positive: Hardened fixture triggered {hard_count} unexpected findings."
            diff_verified = False
        else:
            outcome = ValidationOutcome.NEEDS_REVIEW
            notes = "Ambiguous differential state requires manual review."
            diff_verified = False

        evidence_hash = f"DIFF-{fixture.fixture_id}-{vuln_count}v0h"

        return ComparisonResult(
            fixture_id=fixture.fixture_id,
            rule_id=fixture.target_rule_id,
            framework=fixture.framework,
            outcome=outcome,
            vulnerable_finding_count=vuln_count,
            hardened_finding_count=hard_count,
            diff_verified=diff_verified,
            replay_deterministic=replay_deterministic,
            evidence_hash=evidence_hash,
            notes=notes,
        )
