"""
TorusGuard Core Data Models (v0.5.0)
Defines normalized Finding, Evidence, Remediation, Rule, and AuditReport objects.
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Optional, Dict, Any
import datetime
import uuid


class SeverityLevel(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFORMATIONAL = "Informational"


class ConfidenceLevel(str, Enum):
    CONFIRMED = "Confirmed"
    LIKELY = "Likely"
    NEEDS_REVIEW = "Needs Review"
    INFORMATIONAL = "Informational"
    NOT_APPLICABLE = "Not Applicable"


class LifecycleStage(str, Enum):
    DETECT = "Detect"
    CLASSIFY = "Classify"
    VERIFY = "Verify"
    REMEDIATE = "Remediate"
    RECHECK = "Recheck"
    ARCHIVE = "Archive"


class FindingStatus(str, Enum):
    OPEN = "Open"
    IN_VERIFICATION = "In Verification"
    REMEDIATION_PROPOSED = "Remediation Proposed"
    REMEDIATED = "Remediated"
    VERIFIED_SAFE = "Verified Safe"
    SUPPRESSED = "Suppressed"
    ARCHIVED = "Archived"


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
class Evidence:
    type: EvidenceType
    location: str
    snippet: str
    rationale: str
    confidence_level: ConfidenceLevel
    context: Optional[str] = None
    is_sufficient_for_confirmed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["type"] = self.type.value if isinstance(self.type, EvidenceType) else self.type
        d["confidence_level"] = (
            self.confidence_level.value
            if isinstance(self.confidence_level, ConfidenceLevel)
            else self.confidence_level
        )
        return d


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
class AffectedArea:
    component: str
    target_path: str
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    symbol: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class VerificationStep:
    step_number: int
    action: str
    expected_result: str
    test_command: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class Finding:
    rule_id: str
    title: str
    category: TaxonomyCategory
    severity: SeverityLevel
    confidence: ConfidenceLevel
    lifecycle_stage: LifecycleStage
    status: FindingStatus
    affected_area: AffectedArea
    rationale: str
    evidence: List[Evidence]
    remediation: Remediation
    verification_steps: List[VerificationStep]
    id: str = field(default_factory=lambda: f"TG-FIND-{uuid.uuid4().hex[:8]}")
    asvs_control: Optional[str] = None
    cwe: Optional[str] = None
    nist_ssdf: Optional[str] = None
    limitations: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")
    updated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "rule_id": self.rule_id,
            "title": self.title,
            "category": self.category.value if isinstance(self.category, TaxonomyCategory) else self.category,
            "severity": self.severity.value if isinstance(self.severity, SeverityLevel) else self.severity,
            "confidence": self.confidence.value if isinstance(self.confidence, ConfidenceLevel) else self.confidence,
            "lifecycle_stage": self.lifecycle_stage.value if isinstance(self.lifecycle_stage, LifecycleStage) else self.lifecycle_stage,
            "status": self.status.value if isinstance(self.status, FindingStatus) else self.status,
            "affected_area": self.affected_area.to_dict(),
            "rationale": self.rationale,
            "evidence": [e.to_dict() for e in self.evidence],
            "remediation": self.remediation.to_dict(),
            "verification_steps": [v.to_dict() for v in self.verification_steps],
            "standards_mapping": {
                "asvs_v4": self.asvs_control,
                "cwe": self.cwe,
                "nist_ssdf": self.nist_ssdf,
            },
            "limitations": self.limitations,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class AuditReport:
    project_name: str
    detected_stack: Dict[str, Any]
    findings: List[Finding]
    summary_counts: Dict[str, int] = field(default_factory=dict)
    generated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")
    torusguard_version: str = "v0.5.0"

    def calculate_summary(self) -> None:
        self.summary_counts = {
            "total": len(self.findings),
            "critical": sum(1 for f in self.findings if f.severity == SeverityLevel.CRITICAL),
            "high": sum(1 for f in self.findings if f.severity == SeverityLevel.HIGH),
            "medium": sum(1 for f in self.findings if f.severity == SeverityLevel.MEDIUM),
            "low": sum(1 for f in self.findings if f.severity == SeverityLevel.LOW),
            "confirmed": sum(1 for f in self.findings if f.confidence == ConfidenceLevel.CONFIRMED),
            "likely": sum(1 for f in self.findings if f.confidence == ConfidenceLevel.LIKELY),
            "needs_review": sum(1 for f in self.findings if f.confidence == ConfidenceLevel.NEEDS_REVIEW),
            "remediated": sum(1 for f in self.findings if f.status in (FindingStatus.REMEDIATED, FindingStatus.VERIFIED_SAFE)),
        }

    def to_dict(self) -> Dict[str, Any]:
        self.calculate_summary()
        return {
            "project_name": self.project_name,
            "torusguard_version": self.torusguard_version,
            "generated_at": self.generated_at,
            "detected_stack": self.detected_stack,
            "summary": self.summary_counts,
            "findings": [f.to_dict() for f in self.findings],
        }
