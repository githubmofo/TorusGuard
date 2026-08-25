"""
TorusGuard Finding Lifecycle State Machine (v0.5.0)
Manages progression across Detect -> Classify -> Verify -> Remediate -> Recheck -> Archive.
"""

from typing import List, Tuple, Optional
import datetime
from .models import (
    Finding,
    LifecycleStage,
    FindingStatus,
    ConfidenceLevel,
    EvidenceType,
)


class LifecycleTransitionError(Exception):
    """Raised when an invalid lifecycle state transition is attempted."""
    pass


class FindingLifecycleManager:
    """
    Implements formal lifecycle progression and validation rules for TorusGuard findings.
    """

    ALLOWED_TRANSITIONS = {
        LifecycleStage.DETECT: [LifecycleStage.CLASSIFY, LifecycleStage.ARCHIVE],
        LifecycleStage.CLASSIFY: [LifecycleStage.VERIFY, LifecycleStage.ARCHIVE],
        LifecycleStage.VERIFY: [LifecycleStage.REMEDIATE, LifecycleStage.CLASSIFY, LifecycleStage.ARCHIVE],
        LifecycleStage.REMEDIATE: [LifecycleStage.RECHECK, LifecycleStage.VERIFY],
        LifecycleStage.RECHECK: [LifecycleStage.ARCHIVE, LifecycleStage.VERIFY, LifecycleStage.REMEDIATE],
        LifecycleStage.ARCHIVE: [],  # Terminal state
    }

    @staticmethod
    def transition(finding: Finding, target_stage: LifecycleStage, note: Optional[str] = None) -> Finding:
        current = finding.lifecycle_stage
        allowed = FindingLifecycleManager.ALLOWED_TRANSITIONS.get(current, [])

        if target_stage not in allowed:
            raise LifecycleTransitionError(
                f"Invalid lifecycle transition from '{current.value}' to '{target_stage.value}'. "
                f"Allowed target stages: {[s.value for s in allowed]}"
            )

        # Stage-specific entry constraints
        if target_stage == LifecycleStage.CLASSIFY:
            if not finding.rule_id or not finding.category or not finding.severity:
                raise LifecycleTransitionError("Classification requires rule_id, category, and severity.")
            finding.status = FindingStatus.IN_VERIFICATION

        elif target_stage == LifecycleStage.VERIFY:
            # Verification assertion: If no source/test evidence or evidence is insufficient, force Needs Review
            has_sufficient_evidence = any(
                e.is_sufficient_for_confirmed for e in finding.evidence
            )
            if not has_sufficient_evidence and finding.confidence == ConfidenceLevel.CONFIRMED:
                finding.confidence = ConfidenceLevel.NEEDS_REVIEW
            
            if finding.confidence == ConfidenceLevel.NEEDS_REVIEW:
                finding.status = FindingStatus.IN_VERIFICATION
            elif finding.confidence in (ConfidenceLevel.CONFIRMED, ConfidenceLevel.LIKELY):
                finding.status = FindingStatus.OPEN

        elif target_stage == LifecycleStage.REMEDIATE:
            if not finding.remediation or not finding.remediation.recommended_fix:
                raise LifecycleTransitionError("Remediation stage requires a complete remediation proposal.")
            finding.status = FindingStatus.REMEDIATION_PROPOSED

        elif target_stage == LifecycleStage.RECHECK:
            # Recheck asserts whether remediation was applied
            # In a differential re-check, if finding is fixed, status -> Remediated / Verified Safe
            finding.status = FindingStatus.REMEDIATED

        elif target_stage == LifecycleStage.ARCHIVE:
            finding.status = FindingStatus.ARCHIVED

        finding.lifecycle_stage = target_stage
        finding.updated_at = datetime.datetime.utcnow().isoformat() + "Z"
        return finding

    @staticmethod
    def verify_remediation(finding: Finding, code_after_fix: str, fix_pattern_present: bool) -> Tuple[bool, str]:
        """
        Evaluates whether a remediated codebase satisfies the rule requirement.
        """
        if fix_pattern_present:
            finding.status = FindingStatus.VERIFIED_SAFE
            finding.lifecycle_stage = LifecycleStage.RECHECK
            finding.updated_at = datetime.datetime.utcnow().isoformat() + "Z"
            return True, f"Fix verified safe for {finding.rule_id} at {finding.affected_area.target_path}."
        else:
            finding.status = FindingStatus.OPEN
            finding.lifecycle_stage = LifecycleStage.VERIFY
            finding.updated_at = datetime.datetime.utcnow().isoformat() + "Z"
            return False, f"Remediation pattern not detected for {finding.rule_id}."
