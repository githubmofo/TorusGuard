"""
TorusGuard v0.7.0 Replayable Validation Traces Engine
Records and deterministically replays runtime verification sequences to prove
that vulnerabilities or remediations are reliably reproducible.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict

from core.runtime_evidence import RedactionEngine
from core.runtime_validator import WebValidator


@dataclass
class ReplayStep:
    step_number: int
    action_type: str  # "http_request", "status_assert", "header_assert"
    target: str
    method: str = "GET"
    headers: Optional[Dict[str, str]] = None
    expected_status: Optional[int] = None
    expected_pattern: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ReplayTrace:
    trace_id: str
    finding_id: str
    created_at: str
    target_base_url: str
    description: str
    steps: List[ReplayStep]

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["steps"] = [s.to_dict() for s in self.steps]
        return d


class ReplayManager:
    """
    Manages recording and re-executing deterministic validation sequences.
    """

    def __init__(self, finding_id: str, target_base_url: str, description: str = ""):
        self.trace_id = f"TRC-{finding_id}"
        self.finding_id = finding_id
        self.target_base_url = target_base_url
        self.description = description
        self.steps: List[ReplayStep] = []

    def add_step(
        self,
        action_type: str,
        target: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        expected_status: Optional[int] = None,
        expected_pattern: Optional[str] = None
    ):
        sanitized_headers = RedactionEngine.redact_headers(headers)
        step = ReplayStep(
            step_number=len(self.steps) + 1,
            action_type=action_type,
            target=target,
            method=method.upper(),
            headers=sanitized_headers,
            expected_status=expected_status,
            expected_pattern=expected_pattern
        )
        self.steps.append(step)

    def to_trace(self) -> ReplayTrace:
        return ReplayTrace(
            trace_id=self.trace_id,
            finding_id=self.finding_id,
            created_at=datetime.now(timezone.utc).isoformat(),
            target_base_url=self.target_base_url,
            description=self.description,
            steps=self.steps
        )

    def write_artifacts(self, run_dir: Path) -> Tuple[Path, Path]:
        run_dir.mkdir(parents=True, exist_ok=True)
        json_file = run_dir / "replay.json"
        md_file = run_dir / "replay.md"

        trace = self.to_trace()

        # 1. Write replay.json
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(trace.to_dict(), f, indent=2)

        # 2. Write replay.md
        lines = [
            f"# TorusGuard v0.7.0 Replayable Verification Trace: `{self.finding_id}`",
            f"\n**Trace ID:** `{self.trace_id}`",
            f"**Target Base URL:** `{self.target_base_url}`",
            f"**Total Steps:** `{len(self.steps)}`",
            f"**Description:** {self.description or 'Deterministic runtime verification trace.'}",
            "\n---",
            "\n## 🔁 Execution Steps\n",
            "| Step | Action | Method | Target Path / URI | Expected Status | Assertion Pattern |",
            "|:---:|---|:---:|---|:---:|---|",
        ]
        for s in self.steps:
            lines.append(
                f"| {s.step_number} | `{s.action_type}` | `{s.method}` | `{s.target}` | `{s.expected_status or '-'}` | `{s.expected_pattern or '-'}` |"
            )

        lines.extend([
            "\n---",
            "\n## 🚀 Replay Instructions",
            "To execute this deterministic verification trace via the TorusGuard CLI:",
            "```bash",
            f"python -m core.replay_runner --trace runs/<run-id>/replay.json",
            "```"
        ])

        with open(md_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

        return json_file, md_file

    @classmethod
    def execute_replay(cls, trace: ReplayTrace, validator: WebValidator) -> Dict[str, Any]:
        """
        Re-executes the trace steps against the target application to verify reproducibility.
        """
        results = []
        all_passed = True

        for step in trace.steps:
            target_url = step.target
            if not target_url.startswith("http"):
                target_url = f"{trace.target_base_url.rstrip('/')}/{step.target.lstrip('/')}"

            status, headers, body, decision = validator.execute_probe(
                finding_id=trace.finding_id,
                cluster_id="cluster-replay",
                method=step.method,
                target_url=target_url,
                headers=step.headers,
                expected_status=step.expected_status
            )

            step_passed = True
            reason = "Success"

            if step.expected_status and status != step.expected_status:
                step_passed = False
                reason = f"Status mismatch: expected {step.expected_status}, got {status}"
                all_passed = False

            if step.expected_pattern and step.expected_pattern not in body:
                step_passed = False
                reason = f"Pattern mismatch: '{step.expected_pattern}' not found in response"
                all_passed = False

            results.append({
                "step": step.step_number,
                "passed": step_passed,
                "status_code": status,
                "reason": reason
            })

        return {
            "trace_id": trace.trace_id,
            "reproducible": all_passed,
            "total_steps": len(trace.steps),
            "step_results": results
        }
