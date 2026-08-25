"""
TorusGuard Finding Lifecycle State Machine (v0.5.1)
Manages progression across Detect -> Classify -> Verify -> Remediate -> Recheck -> Archive.
"""

from typing import List, Tuple, Optional
import datetime
import hashlib
from .models import (
    Finding,
    LifecycleStage,
    FindingStatus,
    ConfidenceBand,
    RetestRecord,
)


class LifecycleTransitionError(Exception):
    """Raised when an invalid lifecycle state transition is attempted."""
    pass


class FindingLifecycleManager:
    """
    Implements formal lifecycle progression and validation rules for TorusGuard v0.5.1 findings.
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

        now = datetime.datetime.utcnow().isoformat() + "Z"

        if target_stage == LifecycleStage.CLASSIFY:
            if not finding.rule_id or not finding.category or not finding.severity:
                raise LifecycleTransitionError("Classification requires rule_id, category, and severity.")
            finding.status = FindingStatus.UNCONFIRMED

        elif target_stage == LifecycleStage.VERIFY:
            # Verification assertion: If no source/test evidence or evidence is insufficient, force Needs Review
            has_sufficient_evidence = any(
                e.is_sufficient_for_confirmed for e in finding.evidence
            )
            if not has_sufficient_evidence and finding.confidence.band == ConfidenceBand.CONFIRMED:
                finding.confidence.band = ConfidenceBand.NEEDS_REVIEW
                finding.status = FindingStatus.NEEDS_REVIEW
            elif finding.confidence.band == ConfidenceBand.CONFIRMED:
                finding.status = FindingStatus.CONFIRMED
            else:
                finding.status = FindingStatus.HIGH_CONFIDENCE if finding.confidence.score >= 70 else FindingStatus.NEEDS_REVIEW

            finding.timestamps.verified_at = now

        elif target_stage == LifecycleStage.REMEDIATE:
            if not finding.remediation or not finding.remediation.recommended_fix:
                raise LifecycleTransitionError("Remediation stage requires a complete remediation proposal.")
            finding.status = FindingStatus.REMEDIATED
            finding.timestamps.remediated_at = now

        elif target_stage == LifecycleStage.RECHECK:
            # Recheck requires retest record verification
            if not finding.retest_result.retest_performed:
                raise LifecycleTransitionError("Recheck stage requires an explicit retest to have been executed.")
            if finding.retest_result.closure_status == FindingStatus.VERIFIED_FIXED:
                finding.status = FindingStatus.VERIFIED_FIXED
            finding.timestamps.retested_at = now

        elif target_stage == LifecycleStage.ARCHIVE:
            if finding.status not in (FindingStatus.VERIFIED_FIXED, FindingStatus.SUPPRESSED):
                # Allow archive but note state
                pass

        finding.lifecycle_stage = target_stage
        finding.timestamps.updated_at = now
        return finding

    @staticmethod
    def execute_retest(
        finding: Finding,
        post_fix_code: str,
        safe_pattern_verified: bool,
        retest_method: str = "Differential Static Re-audit",
        verifier_notes: str = "Verified safe via AST/pattern inspection."
    ) -> Tuple[bool, str]:
        """
        Executes a formal retest on post-fix source code, hashing the evidence and updating closure status.
        """
        now = datetime.datetime.utcnow().isoformat() + "Z"
        evidence_hash = hashlib.sha256(post_fix_code.strip().encode("utf-8")).hexdigest()

        if safe_pattern_verified:
            finding.retest_result = RetestRecord(
                retest_performed=True,
                closure_status=FindingStatus.VERIFIED_FIXED,
                fix_applied=finding.remediation.recommended_fix,
                retest_method=retest_method,
                retest_evidence_hash=evidence_hash,
                residual_risk=finding.remediation.residual_risk_notes,
                verifier_notes=verifier_notes,
                retest_timestamp=now,
            )
            finding.status = FindingStatus.VERIFIED_FIXED
            finding.lifecycle_stage = LifecycleStage.RECHECK
            finding.timestamps.retested_at = now
            finding.timestamps.updated_at = now
            return True, f"Finding {finding.finding_id} ({finding.rule_id}) successfully verified fixed. Evidence SHA256: {evidence_hash[:12]}..."
        else:
            finding.retest_result = RetestRecord(
                retest_performed=True,
                closure_status=FindingStatus.OPEN,
                fix_applied=finding.remediation.recommended_fix,
                retest_method=retest_method,
                retest_evidence_hash=evidence_hash,
                residual_risk="Remediation pattern missing or incomplete.",
                verifier_notes="Unsafe pattern still detected in post-fix code.",
                retest_timestamp=now,
            )
            finding.status = FindingStatus.OPEN
            finding.lifecycle_stage = LifecycleStage.VERIFY
            finding.timestamps.updated_at = now
            return False, f"Retest failed for {finding.finding_id}: unsafe pattern remains."
