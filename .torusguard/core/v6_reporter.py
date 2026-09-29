"""
TorusGuard v6 Report Generator
Generates clean, traceable, Human-First Markdown reports for the v6 workflow:
- summary.md
- findings.md
- remediation.md
- apply-plan.md
- recheck.md
- diff-summary.md
"""

from typing import List, Dict, Any, Optional, Tuple
from core.clustering import RootCauseCluster
from core.bundle import RemediationBundle
from core.governance import PatchPolicyDecision
from core.rechecker import TargetedRecheckResult


class V6Reporter:
    """
    Renders standard Markdown artifacts for TorusGuard v6 run folders.
    """

    @staticmethod
    def render_summary(
        target_name: str,
        run_id: str,
        findings: List[Dict[str, Any]],
        clusters: List[RootCauseCluster],
        recheck_results: Optional[List[TargetedRecheckResult]] = None,
    ) -> str:
        total = len(findings)
        confirmed = sum(1 for f in findings if f.get("confidence_band") == "Confirmed")
        needs_review = sum(1 for f in findings if f.get("confidence_band") == "Needs Review")
        high_conf = sum(1 for f in findings if f.get("confidence_band") == "High Confidence")

        out = []
        out.append(f"# TorusGuard v6 Execution Summary — `{target_name}`\n")
        out.append(f"- **Run ID:** `{run_id}`")
        out.append(f"- **Total Findings Modeled:** {total}")
        out.append(f"- **Confirmed:** {confirmed} | **High Confidence:** {high_conf} | **Needs Review:** {needs_review}")
        out.append(f"- **Root-Cause Clusters:** {len(clusters)}\n")

        out.append("## Root-Cause Clustering Breakdown\n")
        out.append("| Cluster ID | Root-Cause Title | Primary Rule | Findings | Files | Hotspot Module | Severity |")
        out.append("|---|---|---|---:|---:|---|---|")
        for c in clusters:
            hotspot = f"`{c.hotspot_module}`" if c.hotspot_module else "root"
            out.append(
                f"| `{c.cluster_id}` | {c.title} | `{c.primary_rule}` | {len(c.finding_ids)} | {len(c.affected_files)} | {hotspot} | {c.risk_severity} |"
            )
        out.append("\n")

        if recheck_results:
            fixed = sum(1 for r in recheck_results if r.outcome.value == "Confirmed Fixed")
            regressed = sum(1 for r in recheck_results if r.outcome.value == "Regressed")
            out.append("## Targeted Recheck Status\n")
            out.append(f"- **Verified Fixed:** {fixed}/{len(recheck_results)}")
            out.append(f"- **Regressions:** {regressed}\n")

        out.append("## Next Actions\n")
        out.append("1. Run `/torusguard harden` to inspect structured remediation bundles.")
        out.append("2. Run `/torusguard apply` to execute Ponytail-governed minimal code modifications.")
        out.append("3. Run `/torusguard recheck` to verify impacted trust boundaries.\n")

        return "\n".join(out)

    @staticmethod
    def render_findings(findings: List[Dict[str, Any]]) -> str:
        out = ["# TorusGuard v6 Detailed Findings\n"]
        total = len(findings)
        
        # High scale handling: if more than 25 findings, show top 15 directly and collapse the rest
        collapse_threshold = 25
        top_findings = findings[:15] if total > collapse_threshold else findings
        overflow_findings = findings[15:] if total > collapse_threshold else []

        for f in top_findings:
            f_id = f.get("finding_id", "fnd-01")
            rule_id = f.get("rule_id", "TG-GENERIC")
            title = f.get("title", "Security Flaw")
            severity = f.get("severity", "High")
            conf_score = f.get("confidence_score", 85)
            conf_band = f.get("confidence_band", "High Confidence")
            cluster_id = f.get("cluster_id", "cluster-general")
            priority = f.get("priority", "Near-Term (P1)")

            target = f.get("target", {})
            file_path = target.get("file_path", "unknown")
            start_line = target.get("line_start", 1)
            end_line = target.get("line_end", start_line)

            evidence = f.get("evidence", {}).get("code_snippet", "# code")

            out.append(f"### 🚨 [{rule_id}] {title}\n")
            out.append(f"- **Stable Finding ID:** `{f_id}`")
            out.append(f"- **Root-Cause Cluster:** `{cluster_id}`")
            out.append(f"- **Severity:** {severity} | **Priority:** {priority}")
            out.append(f"- **Confidence:** {conf_score}/100 ({conf_band})")
            out.append(f"- **Location:** `{file_path}:{start_line}-{end_line}`\n")
            out.append("#### Evidence")
            out.append("```python")
            out.append(evidence.strip())
            out.append("```\n")

            out.append("<details><summary><b>🎫 Ticket Payload</b></summary>\n")
            out.append(f"**Issue:** [{rule_id}] {title} in `{file_path}`\n")
            out.append(f"**Severity:** {severity} | **Priority:** {priority}\n")
            out.append(f"**Finding ID:** `{f_id}`\n")
            out.append("</details>\n")
            out.append("---\n")

        if overflow_findings:
            out.append(f"\n## 📦 Collapsed High-Density Findings ({len(overflow_findings)} additional items)\n")
            out.append("<details><summary><b>Click to expand remaining findings table</b></summary>\n\n")
            out.append("| Finding ID | Rule ID | Title | File Path | Confidence | Cluster |\n")
            out.append("|---|---|---|---|---|---|\n")
            for of in overflow_findings:
                of_id = of.get("finding_id", "")
                of_rule = of.get("rule_id", "")
                of_title = of.get("title", "")
                of_path = of.get("target", {}).get("file_path", "")
                of_conf = f"{of.get('confidence_score', 80)}/100"
                of_cluster = of.get("cluster_id", "")
                out.append(f"| `{of_id}` | `{of_rule}` | {of_title} | `{of_path}` | {of_conf} | `{of_cluster}` |\n")
            out.append("\n</details>\n\n---\n")

        return "\n".join(out)

    @staticmethod
    def render_remediation(bundles: List[RemediationBundle]) -> str:
        out = ["# TorusGuard v6 Remediation Bundles\n"]
        for b in bundles:
            out.append(f"## 🛠️ Bundle: `{b.bundle_id}` — {b.title}\n")
            out.append(f"- **Target Finding:** `{b.finding_id}` (`{b.rule_id}`)")
            if b.cluster_id:
                out.append(f"- **Cluster:** `{b.cluster_id}`")
            out.append(f"- **Target Files:** {', '.join(f'`{tf}`' for tf in b.target_files)}\n")
            out.append("### What Is Wrong")
            out.append(f"{b.what_is_wrong}\n")
            out.append("### What Should Change")
            out.append(f"{b.what_should_change}\n")
            out.append("### Proposed Minimal Diff")
            out.append("```diff")
            out.append(b.proposed_diff.strip())
            out.append("```\n")
            out.append("### Verification After Change")
            out.append(f"{b.verification_steps}\n")
            out.append("---\n")

        return "\n".join(out)

    @staticmethod
    def render_apply_plan(decisions: List[Tuple[str, PatchPolicyDecision]]) -> str:
        out = ["# TorusGuard v6 Minimal Patch Governance & Apply Plan\n"]
        out.append("| Finding / Patch | Files | Added | Deleted | Escalation | Auto-Apply Allowed | Policy Notes |")
        out.append("|---|---:|---:|---:|:---:|:---:|---|")
        for f_id, d in decisions:
            escalation = "⚠️ Yes" if d.escalation_required else "No"
            allowed = "✅ Permitted" if d.allowed_auto_apply else "❌ Blocked (Manual Review)"
            notes = "; ".join(d.rejection_reasons or d.risk_factors or ["Compliant"])
            out.append(
                f"| `{f_id}` | {d.files_touched} | +{d.line_additions} | -{d.line_deletions} | {escalation} | {allowed} | {notes} |"
            )
        out.append("\n")
        return "\n".join(out)

    @staticmethod
    def render_recheck(results: List[TargetedRecheckResult]) -> str:
        out = ["# TorusGuard v6 Targeted Recheck Report\n"]
        out.append("| Finding ID | Rule ID | Target File | Outcome | Regressions | Details |")
        out.append("|---|---|---|---|---|---|")
        for r in results:
            outcome_badge = f"**{r.outcome.value}**"
            reg = "None" if not r.regressions_detected else ", ".join(r.regressions_detected)
            out.append(
                f"| `{r.finding_id}` | `{r.rule_id}` | `{r.target_file}` | {outcome_badge} | {reg} | {r.explanation} |"
            )
        out.append("\n")
        return "\n".join(out)
