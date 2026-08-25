"""
TorusGuard Validation Engine (v0.5.2)
Modular validation subsystem for deterministic fixture replay, differential analysis, and regression tracking.
"""

from .models import (
    ValidationOutcome,
    FixtureDefinition,
    FixtureVariant,
    ReplayResult,
    ComparisonResult,
    RegressionRecord,
    ValidationRunReport,
)
from .fixture_manager import FixtureManager
from .replay_runner import ReplayRunner
from .comparator import ResultComparator
from .regression_tracker import RegressionTracker
from .fp_analyzer import FalsePositiveAnalyzer
from .evidence_collector import ValidationEvidenceCollector
from .report_emitter import ValidationReportEmitter

__version__ = "0.5.2"
__all__ = [
    "ValidationOutcome",
    "FixtureDefinition",
    "FixtureVariant",
    "ReplayResult",
    "ComparisonResult",
    "RegressionRecord",
    "ValidationRunReport",
    "FixtureManager",
    "ReplayRunner",
    "ResultComparator",
    "RegressionTracker",
    "FalsePositiveAnalyzer",
    "ValidationEvidenceCollector",
    "ValidationReportEmitter",
]
