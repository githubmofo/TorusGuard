"""
TorusGuard Core Architecture & Workflow Engine (v0.5.1)
Provides normalized finding models, provenance chains, auditable confidence scoring, and explicit retest state management.
"""

from .models import (
    Finding,
    Evidence,
    Remediation,
    FrameworkPattern,
    AffectedComponent,
    ReproductionMethod,
    RetestRecord,
    NotesRecord,
    FindingTimestamps,
    ProvenanceChain,
    ConfidenceScore,
    ConfidenceFactors,
    ConfidenceBand,
    SeverityLevel,
    SeverityInfo,
    FindingStatus,
    LifecycleStage,
    TaxonomyCategory,
    EvidenceType,
    AuditReport,
)
from .lifecycle import FindingLifecycleManager, LifecycleTransitionError
from .formatter import ReportFormatter

__version__ = "0.5.1"
__all__ = [
    "Finding",
    "Evidence",
    "Remediation",
    "FrameworkPattern",
    "AffectedComponent",
    "ReproductionMethod",
    "RetestRecord",
    "NotesRecord",
    "FindingTimestamps",
    "ProvenanceChain",
    "ConfidenceScore",
    "ConfidenceFactors",
    "ConfidenceBand",
    "SeverityLevel",
    "SeverityInfo",
    "FindingStatus",
    "LifecycleStage",
    "TaxonomyCategory",
    "EvidenceType",
    "AuditReport",
    "FindingLifecycleManager",
    "LifecycleTransitionError",
    "ReportFormatter",
]
