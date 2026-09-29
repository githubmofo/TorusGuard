"""
TorusGuard v0.7.0 Unified Reporting Engine
Combines static code analysis with runtime validation evidence, exploitability confidence,
affected routes, remediation updates, and residual risk assessments into actionable Markdown.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from pathlib import Path


class V070Reporter:
    """
    Renders combined static + runtime validation reports for TorusGuard v0.7.0.
    """

    @classmethod
    def render_combined_summary(
        cls,
        target_name: str,
        run_id: str,
        auth_id: str,
        static_findings: List[Dict[str, Any]],
        runtime_results: List[Dict[str, Any]],
        clusters: List[Any],
        manual_review_items: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        now = datetime.now(timezone.utc).strftime("%B %d, %Y")
        confirmed_count = sum(1 for r in runtime_results if r.get("status") == "Runtime Confirmed")
        likely_count = sum(1 for r in runtime_results if r.get("status") == "Runtime Likely")
        not_repro_count = sum(1 for r in runtime_results if r.get("status") == "Not Reproducible in Scope")
        blocked_count = sum(1 for r in runtime_results if r.get("status") == "Blocked by Environment / Controls")

        lines = [
            f"# TorusGuard v0.7.0 Unified Security & Runtime Exploitability Report",
            f"\n**Target Application:** `{target_name}`",
            f"**Run Identifier:** `{run_id}`",
            f"**Authorization Reference:** `{auth_id}`",
            f"**Execution Date:** {now}",
            f"**Static Findings Detected:** `{len(static_findings)}`",
            f"**Runtime Confirmed Exploitable:** `{confirmed_count}`",
            f"**Runtime Likely Exploitable:** `{likely_count}`",
            f"**Not Reproducible at Runtime:** `{not_repro_count}`",
            f"**Blocked by Controls/Safety:** `{blocked_count}`",
            "\n---",
            "\n## 🎯 Executive Summary & Exploitability Breakdown",
            "\nThis report pairs static source-code analysis with authorized, bounded runtime validation to distinguish theoretical risks from practically reachable and exploitable vulnerabilities.",
            "\n| Metric | Count | Governance Status |",
            "|---|:---:|---|",
            f"| **Runtime Confirmed Exploitable** | `{confirmed_count}` | 🔴 **Immediate Remediation Required** (Reproducible in live scope) |",
            f"| **Runtime Likely** | `{likely_count}` | 🟠 High Priority (Strong behavioral indicators observed) |",
            f"| **Needs Manual Review** | `{len(manual_review_items or [])}` | 🟡 Engineer Sign-Off Required (Ambiguous boundary) |",
            f"| **Not Reproducible in Scope** | `{not_repro_count}` | 🟢 Mitigated at Runtime (Gateway / Middleware active) |",
            f"| **Blocked by Environment / Controls** | `{blocked_count}` | ⚪ Safety Gate Halted Active Probing |",
            "\n---",
            "\n## 🌐 Endpoint & Route Exploitability Matrix\n",
            "| Finding ID | Rule ID | Target Endpoint | Static Severity | Runtime Exploitability | Reproducible? |",
            "|---|---|---|:---:|:---:|:---:|",
        ]

        rt_map = {r.get("finding_id"): r for r in runtime_results}
        for f in static_findings:
            f_id = f.get("finding_id")
            rt = rt_map.get(f_id, {})
            probe_url = rt.get("probe_url", f.get("target", {}).get("file_path", "N/A"))
            status = rt.get("status", "Not Evaluated")
            repro = "✅ Yes" if rt.get("reproducible") else "❌ No"
            lines.append(
                f"| `{f_id}` | `{f.get('rule_id')}` | `{probe_url}` | {f.get('severity', 'Medium')} | **{status}** | {repro} |"
            )

        lines.extend([
            "\n---",
            "\n## 🛡️ Root-Cause Cluster Remediation Plans\n",
        ])

        for c in clusters:
            c_id = getattr(c, "cluster_id", "cluster-general")
            c_title = getattr(c, "title", "General Cluster")
            c_findings = getattr(c, "finding_ids", [])
            lines.extend([
                f"### Root Cause: `{c_id}` — {c_title}",
                f"- **Affected Finding Count:** `{len(c_findings)}` findings",
                f"- **Systemic Fix Advice:** {getattr(c, 'remediation_advice', 'Follow minimal patch guidelines.')}",
                ""
            ])

        if manual_review_items:
            lines.extend([
                "\n---",
                "\n## ⚠️ Manual-Review Items & Residual Risk Queue\n",
            ])
            for item in manual_review_items:
                lines.append(f"- **Finding `{item.get('finding_id')}`:** {item.get('reason', 'Requires human confirmation.')}")

        lines.extend([
            "\n---",
            "\n## 🔒 Safety & Governance Audit Statement",
            "All runtime probes documented in this report were executed under strict target authorization and non-destructive safety gates. No state-destroying actions, unauthorized hosts, or weaponized exploit chains were utilized.",
        ])

        return "\n".join(lines) + "\n"
