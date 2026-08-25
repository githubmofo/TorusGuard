"""
TorusGuard Core Architecture & Workflow Engine (v0.5.4)
Provides normalized finding models, provenance chains, auditable confidence scoring, prioritized remediations, and ticket-ready reports.
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
    RemediationPriority,
    FindingStatus,
    LifecycleStage,
    TaxonomyCategory,
    EvidenceType,
    AuditReport,
    mask_sensitive_data,
)
from .lifecycle import FindingLifecycleManager, LifecycleTransitionError
from .formatter import ReportFormatter

__version__ = "0.5.4"
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
    "RemediationPriority",
    "FindingStatus",
    "LifecycleStage",
    "TaxonomyCategory",
    "EvidenceType",
    "AuditReport",
    "mask_sensitive_data",
    "FindingLifecycleManager",
    "LifecycleTransitionError",
    "ReportFormatter",
]
