"""
TorusGuard v0.7.0 Role-Based Multi-Agent Workflow Engine
Coordinates explicit handoff contracts between Profiler, Validator, Remediator,
and Reviewer agent roles, ensuring strict authority separation and full auditability.
"""

import json
from enum import Enum
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict


class AgentRole(str, Enum):
    PROFILER = "Profiler"
    VALIDATOR = "Validator"
    REMEDIATOR = "Remediator"
    REVIEWER = "Reviewer"


@dataclass
class RoleHandoff:
    handoff_id: str
    from_role: str
    to_role: str
    timestamp: str
    contract_goal: str
    inputs_passed: Dict[str, Any]
    outputs_produced: Dict[str, Any]
    status: str = "Completed"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class RoleOrchestrator:
    """
    Coordinates the 4-role multi-agent workflow and records audit logs.
    """

    def __init__(self, run_id: str):
        self.run_id = run_id
        self.handoffs: List[RoleHandoff] = []

    def record_handoff(
        self,
        from_role: AgentRole,
        to_role: AgentRole,
        contract_goal: str,
        inputs: Dict[str, Any],
        outputs: Dict[str, Any]
    ) -> RoleHandoff:
        now = datetime.now(timezone.utc).isoformat()
        h_id = f"HDF-{len(self.handoffs) + 1:02d}"
        handoff = RoleHandoff(
            handoff_id=h_id,
            from_role=from_role.value,
            to_role=to_role.value,
            timestamp=now,
            contract_goal=contract_goal,
            inputs_passed=inputs,
            outputs_produced=outputs,
            status="Completed"
        )
        self.handoffs.append(handoff)
        return handoff

    def write_artifacts(self, run_dir: Path) -> Tuple[Path, Path]:
        run_dir.mkdir(parents=True, exist_ok=True)
        audit_file = run_dir / "role-audit.json"
        handoff_file = run_dir / "agent-handoffs.md"

        # 1. role-audit.json
        with open(audit_file, "w", encoding="utf-8") as f:
            json.dump([h.to_dict() for h in self.handoffs], f, indent=2)

        # 2. agent-handoffs.md
        lines = [
            "# TorusGuard v0.7.0 Multi-Agent Role Handoff & Governance Trail",
            f"\n**Run Identifier:** `{self.run_id}`",
            f"**Total Role Handoffs:** `{len(self.handoffs)}`",
            "\n---",
            "\n## 👥 Multi-Agent Responsibility Matrix\n",
            "| Agent Role | Explicit Authority & Purpose | Forbidden Actions |",
            "|---|---|---|",
            "| **🔍 Profiler** | Detects tech stack, framework versions, route ASTs, and storage boundaries. | Cannot execute active probes or generate code patches. |",
            "| **⚡ Validator** | Executes authorized, bounded runtime HTTP/browser probes; gathers evidence. | Cannot apply code changes or override reviewer policies. |",
            "| **🛠️ Remediator** | Formulates minimal bounded remediation bundles enriched with runtime context. | Cannot dispatch runtime network probes or declare final sign-off. |",
            "| **🛡️ Reviewer** | Verifies technical evidence, reviews safety decisions, and issues sign-off. | Does not execute probes or author patches. |",
            "\n---",
            "\n## 🔄 Chronological Handoff Log\n",
            "| Handoff ID | From Role | To Role | Contract Goal | Timestamp | Status |",
            "|---|---|---|---|---|:---:|",
        ]
        for h in self.handoffs:
            lines.append(
                f"| `{h.handoff_id}` | **{h.from_role}** | **{h.to_role}** | {h.contract_goal} | `{h.timestamp}` | ✅ {h.status} |"
            )

        with open(handoff_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

        return audit_file, handoff_file
