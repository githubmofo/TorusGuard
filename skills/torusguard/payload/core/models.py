"""
TorusGuard Core Data Models (v0.5.4)
Defines canonical Finding, ProvenanceChain, ConfidenceScore, EvidencePackage, RetestRecord, RemediationPriority, and AuditReport objects.
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Optional, Dict, Any
import datetime
import hashlib
import uuid
import re


class SeverityLevel(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFORMATIONAL = "Informational"


class RemediationPriority(str, Enum):
    IMMEDIATE = "Immediate (P0)"     # Block deployment / immediate fix
    NEAR_TERM = "Near-Term (P1)"     # Fix in current sprint / patch cycle
    BACKLOG = "Backlog (P2)"         # Defense-in-depth hardening backlog


class ConfidenceBand(str, Enum):
    CONFIRMED = "Confirmed"                  # 90 - 100
    HIGH_CONFIDENCE = "High Confidence"      # 70 - 89
    MEDIUM_CONFIDENCE = "Medium Confidence"  # 50 - 69
    LOW_CONFIDENCE = "Low Confidence"        # < 50
    UNCONFIRMED = "Unconfirmed"
    NEEDS_REVIEW = "Needs Review"
    INFORMATIONAL = "Informational"
    NOT_APPLICABLE = "Not Applicable"


class FindingStatus(str, Enum):
    CONFIRMED = "Confirmed"
    HIGH_CONFIDENCE = "High Confidence"
    MEDIUM_CONFIDENCE = "Medium Confidence"
    LOW_CONFIDENCE = "Low Confidence"
    UNCONFIRMED = "Unconfirmed"
    NEEDS_REVIEW = "Needs Review"
    REMEDIATED = "Remediated"
    VERIFIED_FIXED = "Verified Fixed"
    SUPPRESSED = "Suppressed"


class LifecycleStage(str, Enum):
    DETECT = "Detect"
    CLASSIFY = "Classify"
    VERIFY = "Verify"
    REMEDIATE = "Remediate"
    RECHECK = "Recheck"
    ARCHIVE = "Archive"


class TaxonomyCategory(str, Enum):
    AUTH = "authentication-authorization"
    INPUT = "input-validation-encoding"
    DATA = "data-access-orm"
    FILES = "file-upload-handling"
    SECRETS = "secrets-configuration"
    SUPPLY_CHAIN = "dependency-supply-chain"
    NETWORK = "network-ssrf-boundaries"
    BUSINESS_LOGIC = "business-logic-rate-limiting"
    CLIENT_PLATFORM = "client-cache-platform"


class EvidenceType(str, Enum):
    SOURCE = "source"
    RUNTIME = "runtime"
    TEST = "test"
    MANUAL_REVIEW = "manual_review"


@dataclass
class ProvenanceChain:
    discovery_module: str
    triggering_input: str
    evidence_collected: List[str]
    decision_path: List[str]
    verification_step: str
    agent_environment: str = "TorusGuard Engine v0.5.4"
    timestamp: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ConfidenceFactors:
    evidence_quality: int           # Max: 35
    reproduction_success: int       # Max: 25
    independent_confirmations: int  # Max: 15
    environmental_clarity: int      # Max: 15
    manual_review_status: int       # Max: 10

    def total_score(self) -> int:
        return max(0, min(100, (
            self.evidence_quality +
            self.reproduction_success +
            self.independent_confirmations +
            self.environmental_clarity +
            self.manual_review_status
        )))


@dataclass
class ConfidenceScore:
    factors: ConfidenceFactors
    score: int = field(init=False)
    band: ConfidenceBand = field(init=False)
    rationale: str = ""

    def __post_init__(self):
        self.score = self.factors.total_score()
        if self.score >= 90:
            self.band = ConfidenceBand.CONFIRMED
        elif self.score >= 70:
            self.band = ConfidenceBand.HIGH_CONFIDENCE
        elif self.score >= 50:
            self.band = ConfidenceBand.MEDIUM_CONFIDENCE
        else:
            self.band = ConfidenceBand.LOW_CONFIDENCE

    @staticmethod
    def calculate(
        evidence_quality: int = 30,
        reproduction_success: int = 25,
        independent_confirmations: int = 15,
        environmental_clarity: int = 15,
        manual_review_status: int = 5,
        rationale: str = ""
    ) -> 'ConfidenceScore':
        factors = ConfidenceFactors(
            evidence_quality=evidence_quality,
            reproduction_success=reproduction_success,
            independent_confirmations=independent_confirmations,
            environmental_clarity=environmental_clarity,
            manual_review_status=manual_review_status,
        )
        return ConfidenceScore(factors=factors, rationale=rationale)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "score": self.score,
            "band": self.band.value,
            "factors": asdict(self.factors),
            "rationale": self.rationale,
        }


def mask_sensitive_data(text: str) -> str:
    """Masks secrets, tokens, API keys, and passwords from report output."""
    text = re.sub(r'sk_live_[0-9a-zA-Z_\-]{6,}', 'sk_live_***REDACTED***', text)
    text = re.sub(r'ghp_[0-9a-zA-Z_\-]{6,}', 'ghp_***REDACTED***', text)
    text = re.sub(r'(Bearer\s+)[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+\.?[A-Za-z0-9\-_=]*', r'\1***REDACTED_JWT***', text)

    def redact_kv(m):
        val = m.group(3)
        if "***REDACTED" in val:
            return m.group(0)
        return f"{m.group(1)}{m.group(2)}***REDACTED***{m.group(4)}"

    text = re.sub(
        r'(?i)(secret[_\-\w]*|password|api[_\-\w]*key|token|auth[_\-\w]*key)(\s*[:=]\s*[\'"])([^\'"]{4,})([\'"])',
        redact_kv,
        text
    )
    return text


@dataclass
class Evidence:
    type: EvidenceType
    location: str
    raw_snippet: str
    rationale: str
    confidence_level: ConfidenceBand
    sha256_checksum: str = field(init=False)
    context: Optional[str] = None
    reproduction_notes: Optional[str] = None
    reviewer_notes: Optional[str] = None
    is_sufficient_for_confirmed: bool = False
    collected_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")

    def __post_init__(self):
        self.sha256_checksum = hashlib.sha256(self.raw_snippet.strip().encode("utf-8")).hexdigest()

    def get_masked_snippet(self) -> str:
        return mask_sensitive_data(self.raw_snippet)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value if isinstance(self.type, EvidenceType) else self.type,
            "location": self.location,
            "raw_snippet": self.get_masked_snippet(),
            "sha256_checksum": self.sha256_checksum,
            "collected_at": self.collected_at,
            "context": self.context,
            "rationale": self.rationale,
            "confidence_level": self.confidence_level.value if isinstance(self.confidence_level, ConfidenceBand) else self.confidence_level,
            "reproduction_notes": self.reproduction_notes,
            "reviewer_notes": self.reviewer_notes,
            "is_sufficient_for_confirmed": self.is_sufficient_for_confirmed,
        }


@dataclass
class SeverityInfo:
    level: SeverityLevel
    rationale: str
    rubric_justification: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level.value if isinstance(self.level, SeverityLevel) else self.level,
            "rationale": self.rationale,
            "rubric_justification": self.rubric_justification,
        }


@dataclass
class FrameworkPattern:
    framework: str
    unsafe_snippet: str
    safe_snippet: str
    least_invasive: bool = True


@dataclass
class Remediation:
    problem_statement: str
    risk_explanation: str
    recommended_fix: str
    framework_pattern: FrameworkPattern
    verification_method: str
    residual_risk_notes: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "problem_statement": self.problem_statement,
            "risk_explanation": self.risk_explanation,
            "recommended_fix": self.recommended_fix,
            "framework_pattern": asdict(self.framework_pattern),
            "verification_method": self.verification_method,
            "residual_risk_notes": self.residual_risk_notes,
        }


@dataclass
class AffectedComponent:
    component_name: str
    target_path: str
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    symbol: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class ReproductionMethod:
    step_by_step: List[str]
    deterministic: bool = True
    test_command: Optional[str] = None
    expected_failure_response: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class RetestRecord:
    retest_performed: bool = False
    closure_status: FindingStatus = FindingStatus.UNCONFIRMED
    fix_applied: Optional[str] = None
    retest_method: Optional[str] = None
    retest_evidence_hash: Optional[str] = None
    residual_risk: Optional[str] = None
    verifier_notes: Optional[str] = None
    retest_timestamp: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["closure_status"] = self.closure_status.value if isinstance(self.closure_status, FindingStatus) else self.closure_status
        return {k: v for k, v in d.items() if v is not None}


@dataclass
class NotesRecord:
    business_impact: str
    technical_description: str
    raw_facts_summary: str
    ai_interpretation: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class FindingTimestamps:
    discovered_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")
    updated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")
    verified_at: Optional[str] = None
    remediated_at: Optional[str] = None
    retested_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class Finding:
    rule_id: str
    title: str
    category: TaxonomyCategory
    severity: SeverityInfo
    confidence: ConfidenceScore
    status: FindingStatus
    affected_component: AffectedComponent
    evidence: List[Evidence]
    provenance: ProvenanceChain
    reproduction_method: ReproductionMethod
    remediation: Remediation
    remediation_priority: RemediationPriority = RemediationPriority.IMMEDIATE
    retest_result: RetestRecord = field(default_factory=RetestRecord)
    timestamps: FindingTimestamps = field(default_factory=FindingTimestamps)
    notes: NotesRecord = field(default_factory=lambda: NotesRecord(
        business_impact="Exposure of sensitive application resources or unauthorized data modification.",
        technical_description="Direct unmitigated pattern detected in application route or data layer.",
        raw_facts_summary="Unmitigated pattern identified in source.",
        ai_interpretation="High priority fix recommended.",
    ))
    finding_id: str = field(default_factory=lambda: f"TG-FIND-{datetime.datetime.utcnow().year}-{uuid.uuid4().hex[:6]}")
    lifecycle_stage: LifecycleStage = LifecycleStage.DETECT
    asvs_control: Optional[str] = None
    cwe: Optional[str] = None
    nist_ssdf: Optional[str] = None

    def __post_init__(self):
        # Auto-derive remediation priority from severity level if default
        if self.severity.level == SeverityLevel.CRITICAL:
            self.remediation_priority = RemediationPriority.IMMEDIATE
        elif self.severity.level == SeverityLevel.HIGH:
            self.remediation_priority = RemediationPriority.NEAR_TERM
        else:
            self.remediation_priority = RemediationPriority.BACKLOG

    def to_dict(self) -> Dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "rule_id": self.rule_id,
            "title": self.title,
            "category": self.category.value if isinstance(self.category, TaxonomyCategory) else self.category,
            "severity": self.severity.to_dict(),
            "confidence": self.confidence.to_dict(),
            "status": self.status.value if isinstance(self.status, FindingStatus) else self.status,
            "remediation_priority": self.remediation_priority.value if isinstance(self.remediation_priority, RemediationPriority) else self.remediation_priority,
            "lifecycle_stage": self.lifecycle_stage.value if isinstance(self.lifecycle_stage, LifecycleStage) else self.lifecycle_stage,
            "affected_component": self.affected_component.to_dict(),
            "evidence": [e.to_dict() for e in self.evidence],
            "provenance": self.provenance.to_dict(),
            "reproduction_method": self.reproduction_method.to_dict(),
            "remediation": self.remediation.to_dict(),
            "retest_result": self.retest_result.to_dict(),
            "requirement_reference": {
                "asvs_v4": self.asvs_control,
                "cwe": self.cwe,
                "nist_ssdf": self.nist_ssdf,
            },
            "cwe": self.cwe,
            "timestamps": self.timestamps.to_dict(),
            "notes": self.notes.to_dict(),
        }


@dataclass
class AuditReport:
    project_name: str
    detected_stack: Dict[str, Any]
    findings: List[Finding]
    summary_counts: Dict[str, Any] = field(default_factory=dict)
    generated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")
    torusguard_version: str = "v0.5.4"
    report_owner: str = "TorusGuard Security Subsystem"
    repository_ref: str = "workspace"

    def calculate_summary(self) -> None:
        total = len(self.findings)
        avg_confidence = round(sum(f.confidence.score for f in self.findings) / total, 1) if total > 0 else 100.0
        self.summary_counts = {
            "total_findings": total,
            "average_confidence_score": avg_confidence,
            "critical": sum(1 for f in self.findings if f.severity.level == SeverityLevel.CRITICAL),
            "high": sum(1 for f in self.findings if f.severity.level == SeverityLevel.HIGH),
            "medium": sum(1 for f in self.findings if f.severity.level == SeverityLevel.MEDIUM),
            "low": sum(1 for f in self.findings if f.severity.level == SeverityLevel.LOW),
            "confirmed": sum(1 for f in self.findings if f.confidence.band == ConfidenceBand.CONFIRMED),
            "high_confidence": sum(1 for f in self.findings if f.confidence.band == ConfidenceBand.HIGH_CONFIDENCE),
            "needs_review": sum(1 for f in self.findings if f.confidence.band in (ConfidenceBand.NEEDS_REVIEW, ConfidenceBand.LOW_CONFIDENCE)),
            "verified_fixed": sum(1 for f in self.findings if f.status == FindingStatus.VERIFIED_FIXED),
            "remediated": sum(1 for f in self.findings if f.status in (FindingStatus.REMEDIATED, FindingStatus.VERIFIED_FIXED)),
            "immediate_priority": sum(1 for f in self.findings if f.remediation_priority == RemediationPriority.IMMEDIATE),
            "near_term_priority": sum(1 for f in self.findings if f.remediation_priority == RemediationPriority.NEAR_TERM),
            "backlog_priority": sum(1 for f in self.findings if f.remediation_priority == RemediationPriority.BACKLOG),
        }

    def to_dict(self) -> Dict[str, Any]:
        self.calculate_summary()
        return {
            "project_name": self.project_name,
            "torusguard_version": self.torusguard_version,
            "generated_at": self.generated_at,
            "report_owner": self.report_owner,
            "repository_ref": self.repository_ref,
            "detected_stack": self.detected_stack,
            "summary": self.summary_counts,
            "findings": [f.to_dict() for f in self.findings],
        }
