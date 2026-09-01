"""
TorusGuard v0.7.0 Safety & Approval Gates
Enforces explicit governance gates for sensitive endpoints, privileged actions,
and state-changing runtime operations before execution.
"""

import json
from enum import Enum
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict


class SafetyReviewLevel(str, Enum):
    AUTO_ALLOWED = "Auto-Allowed"
    APPROVAL_REQUIRED = "Approval Required"
    MANUAL_ONLY = "Manual Only"


@dataclass
class SafetyDecision:
    action_id: str
    method: str
    target_path: str
    review_level: str
    allowed_to_proceed: bool
    rationale: str
    requires_human_approval: bool
    escalation_reasons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SafetyGate:
    """
    Evaluates runtime actions and determines whether they are auto-allowed,
    require explicit human/agent approval, or are strictly manual-only.
    """

    CRITICAL_MANUAL_PATHS = [
        "/admin/delete",
        "/admin/users/delete",
        "/system/shutdown",
        "/system/reset",
        "/api/v1/database/drop",
        "/billing/charge",
        "/auth/password-reset-confirm"
    ]

    SENSITIVE_APPROVAL_KEYWORDS = [
        "auth",
        "login",
        "session",
        "token",
        "tenant",
        "upload",
        "transfer",
        "credential",
        "secret",
        "role"
    ]

    @classmethod
    def evaluate_action(
        cls,
        action_id: str,
        method: str,
        path: str,
        context: Optional[str] = None,
        pre_approved: bool = False
    ) -> SafetyDecision:
        """
        Evaluates safety risk and returns a formal SafetyDecision.
        """
        method_upper = method.upper()
        path_lower = path.lower()
        context_lower = (context or "").lower()
        escalations = []

        # 1. Check for Critical / Destructive paths -> Manual Only
        for crit in cls.CRITICAL_MANUAL_PATHS:
            if crit in path_lower or crit in context_lower:
                escalations.append(f"Matches critical path/action pattern '{crit}'")
                return SafetyDecision(
                    action_id=action_id,
                    method=method_upper,
                    target_path=path,
                    review_level=SafetyReviewLevel.MANUAL_ONLY.value,
                    allowed_to_proceed=False,
                    rationale="High-risk destructive/privileged path; automated execution blocked.",
                    requires_human_approval=True,
                    escalation_reasons=escalations
                )

        # 2. Check for State-Changing methods or Sensitive keywords -> Approval Required
        is_state_changing = method_upper in ["POST", "PUT", "DELETE", "PATCH"]
        if is_state_changing:
            escalations.append(f"HTTP method '{method_upper}' can alter server state")

        for kw in cls.SENSITIVE_APPROVAL_KEYWORDS:
            if kw in path_lower or kw in context_lower:
                escalations.append(f"Touches sensitive security context keyword '{kw}'")

        if escalations:
            # Requires approval
            allowed = pre_approved
            rationale = "Pre-approved by security engineer" if pre_approved else "Requires explicit approval before execution"
            return SafetyDecision(
                action_id=action_id,
                method=method_upper,
                target_path=path,
                review_level=SafetyReviewLevel.APPROVAL_REQUIRED.value,
                allowed_to_proceed=allowed,
                rationale=rationale,
                requires_human_approval=not pre_approved,
                escalation_reasons=escalations
            )

        # 3. Read-only standard path -> Auto-Allowed
        return SafetyDecision(
            action_id=action_id,
            method=method_upper,
            target_path=path,
            review_level=SafetyReviewLevel.AUTO_ALLOWED.value,
            allowed_to_proceed=True,
            rationale="Read-only query to non-sensitive in-scope endpoint.",
            requires_human_approval=False,
            escalation_reasons=[]
        )

    @staticmethod
    def record_decisions(run_dir: Path, decisions: List[SafetyDecision]) -> Path:
        run_dir.mkdir(parents=True, exist_ok=True)
        decision_file = run_dir / "safety-decisions.json"
        data = [d.to_dict() for d in decisions]
        with open(decision_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return decision_file
