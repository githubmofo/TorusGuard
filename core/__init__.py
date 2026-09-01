"""
TorusGuard Core Architecture & Security Workflow Engine (v0.7.0)

Tiered architectural layers:
- Tier 1: Canonical Data Models, Lifecycle State Machine & Reporting (v0.5 base)
- Tier 2: Governed Remediation, Clustering, Patch Policy & SARIF Export (v0.6 engine)
- Tier 3: Authorized Runtime Validation, Exploitability Confirmation & Multi-Agent Roles (v0.7 engine)
"""

# ==============================================================================
# Tier 1: Canonical Data Models, Lifecycle & Provenance (v0.5 base)
# ==============================================================================
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
from .run_folder import RunFolder

# ==============================================================================
# Tier 2: Governed Remediation, Clustering, Patch Policy & SARIF (v0.6 engine)
# ==============================================================================
from .identity import IdentityEngine, FindingFingerprint
from .clustering import ClusteringEngine, RootCauseCluster
from .bundle import BundleManager, RemediationBundle
from .governance import PatchGovernor, PatchPolicyDecision, HIGH_RISK_KEYWORDS, SENSITIVE_CATEGORIES
from .rechecker import TargetedRechecker, TargetedRecheckResult, RecheckOutcome
from .run_manager import RunManager
from .sarif import SarifExporter
from .v6_reporter import V6Reporter
from .v6_workflow import V6Workflow
from .stack_profiler import StackProfiler, StackProfile

# ==============================================================================
# Tier 3: Authorized Runtime Validation & Exploitability Confirmation (v0.7 engine)
# ==============================================================================
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
    # Tier 1: Canonical Models & Lifecycle
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
    "RunFolder",
    # Tier 2: Governed Remediation & v0.6 Engine
    "IdentityEngine",
    "FindingFingerprint",
    "ClusteringEngine",
    "RootCauseCluster",
    "BundleManager",
    "RemediationBundle",
    "PatchGovernor",
    "PatchPolicyDecision",
    "HIGH_RISK_KEYWORDS",
    "SENSITIVE_CATEGORIES",
    "TargetedRechecker",
    "TargetedRecheckResult",
    "RecheckOutcome",
    "RunManager",
    "SarifExporter",
    "V6Reporter",
    "V6Workflow",
    "StackProfiler",
    "StackProfile",
    # Tier 3: Authorized Runtime Validation & v0.7 Engine
    "AuthorizationManager",
    "AuthorizationRecord",
    "TargetScope",
    "AuthorizationError",
    "SafetyGate",
    "SafetyDecision",
    "SafetyReviewLevel",
    "EvidenceCollector",
    "RuntimeEvidenceItem",
    "RedactionEngine",
    "WebValidator",
    "SessionState",
    "ExploitChecker",
    "ExploitCheckResult",
    "ExploitabilityStatus",
    "BrowserVerifier",
    "BrowserAction",
    "RoleOrchestrator",
    "RoleHandoff",
    "AgentRole",
    "ReplayManager",
    "ReplayTrace",
    "ReplayStep",
    "V070Reporter",
    "V070Workflow",
]

