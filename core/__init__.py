"""
TorusGuard Core Architecture & Governed Remediation Engine (v0.6.3)
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
from .stack_profiler import StackProfiler, StackProfile
from .authorization import AuthorizationManager, AuthorizationRecord, TargetScope, AuthorizationError
from .safety_gate import SafetyGate, SafetyDecision, SafetyReviewLevel
from .runtime_evidence import EvidenceCollector, RuntimeEvidenceItem, RedactionEngine
from .runtime_validator import WebValidator, SessionState
from .exploit_checker import ExploitChecker, ExploitCheckResult, ExploitabilityStatus
from .browser_verifier import BrowserVerifier, BrowserAction
from .agent_roles import RoleOrchestrator, RoleHandoff, AgentRole
from .replay_trace import ReplayManager, ReplayTrace, ReplayStep
from .v070_reporter import V070Reporter
from .v070_workflow import V070Workflow

__version__ = "0.7.0"
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
    "StackProfiler",
    "StackProfile",
]

