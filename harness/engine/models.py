"""
TorusGuard Validation Engine Data Models (v0.5.2)
Defines structured FixtureDefinition, ReplayResult, ComparisonResult, RegressionRecord, and ValidationRunReport.
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Optional, Dict, Any
import datetime
import hashlib
import uuid


class ValidationOutcome(str, Enum):
    VULNERABLE_CONFIRMED = "Vulnerable Confirmed"
    HARDENED_SAFE = "Hardened Safe"
    FALSE_POSITIVE = "False Positive"
    FALSE_NEGATIVE = "False Negative"
    NEEDS_REVIEW = "Needs Review"
    REGRESSION_DETECTED = "Regression Detected"


@dataclass
class FixtureVariant:
    relative_path: str
    code_pattern: str
    expected_findings_count: int
    is_hardened: bool = False


@dataclass
class FixtureDefinition:
    fixture_id: str
    framework: str
    scenario: str
    target_rule_id: str
    expected_outcome: ValidationOutcome
    vulnerable_variant: FixtureVariant
    hardened_variant: FixtureVariant
    reproduction_command: str
    expected_diff_summary: str
    version_tags: List[str] = field(default_factory=lambda: ["v0.5.0", "v0.5.1", "v0.5.2"])
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "fixture_id": self.fixture_id,
            "framework": self.framework,
            "scenario": self.scenario,
            "target_rule_id": self.target_rule_id,
            "expected_outcome": self.expected_outcome.value,
            "vulnerable_variant": asdict(self.vulnerable_variant),
            "hardened_variant": asdict(self.hardened_variant),
            "reproduction_command": self.reproduction_command,
            "expected_diff_summary": self.expected_diff_summary,
            "version_tags": self.version_tags,
            "notes": self.notes,
        }


@dataclass
class ReplayResult:
    fixture_id: str
    run_count: int
    deterministic: bool
    execution_hashes: List[str]
    inputs_used: Dict[str, Any]
    outputs_produced: Dict[str, Any]
    timestamps: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ComparisonResult:
    fixture_id: str
    rule_id: str
    framework: str
    outcome: ValidationOutcome
    vulnerable_finding_count: int
    hardened_finding_count: int
    diff_verified: bool
    replay_deterministic: bool
    evidence_hash: str
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["outcome"] = self.outcome.value if isinstance(self.outcome, ValidationOutcome) else self.outcome
        return d


@dataclass
class RegressionRecord:
    case_id: str
    historical_version: str
    original_flaw: str
    fix_verified: bool
    regression_status: str  # "Clean", "Regressed", "Needs Review"
    last_verified_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ValidationRunReport:
    run_id: str = field(default_factory=lambda: f"TG-VAL-{datetime.datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}")
    engine_version: str = "v0.5.2"
    timestamp: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")
    environment: Dict[str, str] = field(default_factory=dict)
    summary: Dict[str, int] = field(default_factory=dict)
    fixture_results: List[ComparisonResult] = field(default_factory=list)
    regression_records: List[RegressionRecord] = field(default_factory=list)

    def calculate_summary(self):
        total = len(self.fixture_results)
        self.summary = {
            "total_fixtures": total,
            "passed": sum(1 for r in self.fixture_results if r.outcome in (ValidationOutcome.VULNERABLE_CONFIRMED, ValidationOutcome.HARDENED_SAFE)),
            "failed": sum(1 for r in self.fixture_results if r.outcome in (ValidationOutcome.FALSE_POSITIVE, ValidationOutcome.FALSE_NEGATIVE, ValidationOutcome.REGRESSION_DETECTED)),
            "vulnerable_confirmed": sum(1 for r in self.fixture_results if r.outcome == ValidationOutcome.VULNERABLE_CONFIRMED),
            "hardened_safe": sum(1 for r in self.fixture_results if r.outcome == ValidationOutcome.HARDENED_SAFE),
            "false_positives": sum(1 for r in self.fixture_results if r.outcome == ValidationOutcome.FALSE_POSITIVE),
            "false_negatives": sum(1 for r in self.fixture_results if r.outcome == ValidationOutcome.FALSE_NEGATIVE),
            "needs_review": sum(1 for r in self.fixture_results if r.outcome == ValidationOutcome.NEEDS_REVIEW),
            "regressions_detected": sum(1 for r in self.fixture_results if r.outcome == ValidationOutcome.REGRESSION_DETECTED),
        }

    def to_dict(self) -> Dict[str, Any]:
        self.calculate_summary()
        return {
            "run_id": self.run_id,
            "engine_version": self.engine_version,
            "timestamp": self.timestamp,
            "environment": self.environment,
            "summary": self.summary,
            "fixture_results": [r.to_dict() for r in self.fixture_results],
            "regression_records": [rec.to_dict() for rec in self.regression_records],
        }
