"""
TorusGuard Core Architecture & Governed Remediation Engine (v6.0.0)
Provides stable finding identities, root-cause clustering, remediation bundles,
minimal patch governance, targeted recheck, run folder management, and SARIF exports.
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
from .identity import IdentityEngine, FindingFingerprint
from .clustering import ClusteringEngine, RootCauseCluster
from .bundle import BundleManager, RemediationBundle
from .governance import PatchGovernor, PatchPolicyDecision
from .rechecker import TargetedRechecker, TargetedRecheckResult, RecheckOutcome
from .run_manager import RunManager
from .sarif import SarifExporter
from .v6_reporter import V6Reporter
from .v6_workflow import V6Workflow

__version__ = "6.0.0"
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
    "IdentityEngine",
    "FindingFingerprint",
    "ClusteringEngine",
    "RootCauseCluster",
    "BundleManager",
    "RemediationBundle",
    "PatchGovernor",
    "PatchPolicyDecision",
    "TargetedRechecker",
    "TargetedRecheckResult",
    "RecheckOutcome",
    "RunManager",
    "SarifExporter",
    "V6Reporter",
    "V6Workflow",
]

