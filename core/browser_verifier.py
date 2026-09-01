"""
TorusGuard v0.7.0 Browser-Assisted Verification Engine
Validates client-side route guards, authenticated frontend flows, and DOM/UI evidence
with capped navigation depth, action logging, and safety controls.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

from core.authorization import AuthorizationRecord, AuthorizationManager, AuthorizationError
from core.safety_gate import SafetyGate, SafetyReviewLevel


@dataclass
class BrowserAction:
    action_id: str
    action_type: str  # "navigate", "assert_dom", "check_route_guard", "capture_snapshot"
    target_url: str
    selector: Optional[str] = None
    outcome: str = ""
    dom_snippet: Optional[str] = None
    requires_approval: bool = False
    approved: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class BrowserVerifier:
    """
    Simulates and executes bounded browser-assisted validations against client-side flows.
    """

    def __init__(
        self,
        auth_record: AuthorizationRecord,
        max_depth: int = 3
    ):
        self.auth = auth_record
        self.max_depth = min(max_depth, auth_record.scope.max_depth)
        self.current_depth = 0
        self.action_history: List[BrowserAction] = []

    def verify_route_guard(
        self,
        target_url: str,
        authenticated: bool,
        expected_redirect_url: Optional[str] = None,
        protected_dom_marker: Optional[str] = None,
        client_dom_content: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validates whether client-side router/guards protect sensitive UI components
        or leak them before authentication.
        """
        AuthorizationManager.check_authorized_or_raise(target_url, self.auth, method="GET")

        action_id = f"BRW-{len(self.action_history) + 1:03d}"
        decision = SafetyGate.evaluate_action(action_id, "GET", target_url)

        if not decision.allowed_to_proceed:
            action = BrowserAction(
                action_id=action_id,
                action_type="check_route_guard",
                target_url=target_url,
                outcome="BLOCKED_BY_SAFETY_GATE",
                requires_approval=True,
                approved=False
            )
            self.action_history.append(action)
            return {"status": "Blocked by Safety Gate", "action": action.to_dict()}

        # Evaluate Client-Side DOM Guard
        dom = client_dom_content or ""
        guard_intact = True
        leak_detected = False

        if not authenticated:
            # When unauthenticated, sensitive DOM marker should NOT be present
            if protected_dom_marker and protected_dom_marker in dom:
                guard_intact = False
                leak_detected = True
                outcome = f"Client Route Guard Failed: Sensitive marker '{protected_dom_marker}' rendered without authentication."
            else:
                outcome = "Client Route Guard Enforced: Protected view withheld from unauthenticated DOM."
        else:
            outcome = "Authenticated Session Verified: Client loaded permitted views."

        action = BrowserAction(
            action_id=action_id,
            action_type="check_route_guard",
            target_url=target_url,
            outcome=outcome,
            dom_snippet=dom[:200] if dom else None,
            requires_approval=False,
            approved=True
        )
        self.action_history.append(action)

        return {
            "guard_intact": guard_intact,
            "leak_detected": leak_detected,
            "outcome": outcome,
            "action": action.to_dict()
        }

    def write_report(self, run_dir: Path) -> Path:
        run_dir.mkdir(parents=True, exist_ok=True)
        report_file = run_dir / "browser-validation.md"
        lines = [
            "# TorusGuard v0.7.0 Browser-Assisted Validation Report",
            f"\n**Authorization ID:** `{self.auth.authorization_id}`",
            f"**Max Navigation Depth:** `{self.max_depth}` levels",
            f"**Total Browser Actions:** `{len(self.action_history)}`",
            "\n---",
            "\n## 🖥️ UI Action Traces\n",
            "| Action ID | Type | Target URL | Outcome | Approval Status |",
            "|---|---|---|---|:---:|",
        ]
        for a in self.action_history:
            lines.append(f"| `{a.action_id}` | `{a.action_type}` | `{a.target_url}` | {a.outcome} | **{'Approved' if a.approved else 'Blocked'}** |")

        with open(report_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

        return report_file
