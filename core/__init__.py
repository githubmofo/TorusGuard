"""
TorusGuard Core Architecture & Workflow Engine (v0.5.0)
Provides normalized finding models, lifecycle state management, and evidence validation.
"""

from .models import (
    Finding,
    Evidence,
    Remediation,
    FrameworkPattern,
    AffectedArea,
    VerificationStep,
    LifecycleStage,
    ConfidenceLevel,
    SeverityLevel,
    FindingStatus,
    TaxonomyCategory,
    AuditReport,
)
from .lifecycle import FindingLifecycleManager
from .formatter import ReportFormatter

__version__ = "0.5.0"
__all__ = [
    "Finding",
    "Evidence",
    "Remediation",
    "FrameworkPattern",
    "AffectedArea",
    "VerificationStep",
    "LifecycleStage",
    "ConfidenceLevel",
    "SeverityLevel",
    "FindingStatus",
    "TaxonomyCategory",
    "AuditReport",
    "FindingLifecycleManager",
    "ReportFormatter",
]
