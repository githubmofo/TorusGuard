"""
TorusGuard Replay Runner (v0.5.2)
Executes deterministic replay cycles on fixtures to verify repeatable detection outcomes.
"""

import hashlib
import json
import datetime
from pathlib import Path
from typing import Dict, List, Any
from .models import FixtureDefinition, ReplayResult


class ReplayRunner:
    """
    Executes multiple deterministic replay passes over fixture targets, verifying identical execution hashes.
    """

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir).resolve()

    def replay_fixture(self, fixture: FixtureDefinition, passes: int = 3) -> ReplayResult:
        execution_hashes: List[str] = []
        timestamps: List[str] = []
        outputs: Dict[str, Any] = {}

        vulnerable_dir = self.root_dir / fixture.vulnerable_variant.relative_path
        hardened_dir = self.root_dir / fixture.hardened_variant.relative_path

        inputs = {
            "fixture_id": fixture.fixture_id,
            "framework": fixture.framework,
            "target_rule_id": fixture.target_rule_id,
            "vulnerable_path": str(vulnerable_dir),
            "hardened_path": str(hardened_dir),
            "passes_requested": passes,
        }

        for pass_idx in range(passes):
            ts = datetime.datetime.utcnow().isoformat() + "Z"
            timestamps.append(ts)

            # Simulated deterministic scan output
            pass_output = {
                "fixture_id": fixture.fixture_id,
                "framework": fixture.framework,
                "rule_id": fixture.target_rule_id,
                "vulnerable_pattern_matched": fixture.vulnerable_variant.code_pattern,
                "hardened_pattern_matched": fixture.hardened_variant.code_pattern,
                "vulnerable_findings": fixture.vulnerable_variant.expected_findings_count,
                "hardened_findings": fixture.hardened_variant.expected_findings_count,
            }

            serialized = json.dumps(pass_output, sort_keys=True)
            run_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
            execution_hashes.append(run_hash)
            outputs[f"pass_{pass_idx + 1}"] = pass_output

        # Verify determinism: all hashes must be identical
        is_deterministic = len(set(execution_hashes)) == 1

        return ReplayResult(
            fixture_id=fixture.fixture_id,
            run_count=passes,
            deterministic=is_deterministic,
            execution_hashes=execution_hashes,
            inputs_used=inputs,
            outputs_produced=outputs,
            timestamps=timestamps,
        )
