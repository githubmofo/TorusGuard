"""
TorusGuard v6 Governed Remediation Workflow Controller
Coordinates the complete v6 workflow:
1. Scan & Stable Finding Identity
2. Root-Cause Clustering
3. Structured Remediation Bundles
4. Minimal Patch Governance
5. Targeted Recheck & Regression Verification
6. Run Folder Artifact Emission & SARIF Export
"""

from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from core.identity import IdentityEngine
from core.clustering import ClusteringEngine, RootCauseCluster
from core.bundle import BundleManager, RemediationBundle
from core.governance import PatchGovernor, PatchPolicyDecision
from core.rechecker import TargetedRechecker, TargetedRecheckResult, RecheckOutcome
from core.run_manager import RunManager
from core.sarif import SarifExporter
from core.v6_reporter import V6Reporter


class V6Workflow:
    """
    Unified controller for TorusGuard v6 governed remediation and recheck operations.
    """

    def __init__(self, target_root: Optional[Path] = None, output_base: Optional[Path] = None):
        self.target_root = target_root or Path(".")
        self.output_base = output_base or Path(".torusguard/runs")

    def execute_audit(
        self,
        raw_findings: List[Dict[str, Any]],
        target_name: str = "workspace",
        run_id: Optional[str] = None,
        export_sarif: bool = True,
    ) -> RunManager:
        """
        Executes Phase 1 & 2: Identifies stable fingerprints, clusters root causes, and emits run artifacts.
        """
        run_mgr = RunManager(
            base_dir=self.output_base,
            target_name=target_name,
            command="audit",
            run_id=run_id,
        )

        # 1. Attach Stable Finding Identifiers
        enriched_findings = []
        evidence_list = []

        for f in raw_findings:
            rule_id = f.get("rule_id", "TG-GENERIC")
            target = f.get("target", {})
            file_path = target.get("file_path", "unknown")
            snippet = f.get("evidence", {}).get("code_snippet", "")
            sink = f.get("sink_signature")
            framework = f.get("framework_marker")

            fp = IdentityEngine.generate_identity(
                rule_id=rule_id,
                file_path=file_path,
                code_snippet=snippet,
                sink_signature=sink,
                framework_marker=framework,
                root_path=self.target_root,
            )

            item = dict(f)
            item["finding_id"] = fp.fingerprint_id
            item["fingerprint_id"] = fp.fingerprint_id
            item["region_hash"] = fp.region_hash
            enriched_findings.append(item)

            evidence_list.append({
                "finding_id": fp.fingerprint_id,
                "rule_id": rule_id,
                "file_path": file_path,
                "region_hash": fp.region_hash,
                "code_snippet": snippet,
            })

        # 2. Cluster Findings by Root Cause
        clusters = ClusteringEngine.cluster_findings(enriched_findings)
        cluster_map = {c.primary_rule: c.cluster_id for c in clusters}

        for ef in enriched_findings:
            ef["cluster_id"] = cluster_map.get(ef.get("rule_id"), "cluster-general")

        # 3. Render and Write Standard Artifacts
        summary_md = V6Reporter.render_summary(
            target_name=target_name,
            run_id=run_mgr.run_id,
            findings=enriched_findings,
            clusters=clusters,
        )
        findings_md = V6Reporter.render_findings(enriched_findings)

        run_mgr.write_summary(summary_md)
        run_mgr.write_findings(findings_md)
        run_mgr.write_evidence(evidence_list)

        # 4. Optional SARIF export
        if export_sarif:
            sarif_dict = SarifExporter.generate_sarif(
                findings=enriched_findings,
                clusters=[c.to_dict() for c in clusters],
            )
            run_mgr.write_sarif(sarif_dict)

        # 5. Write Run Manifest
        status_counts = {
            "total_findings": len(enriched_findings),
            "confirmed": sum(1 for f in enriched_findings if f.get("confidence_band") == "Confirmed"),
            "high_confidence": sum(1 for f in enriched_findings if f.get("confidence_band") == "High Confidence"),
            "needs_review": sum(1 for f in enriched_findings if f.get("confidence_band") == "Needs Review"),
            "remediated": 0,
            "verified_fixed": 0,
            "regressed": 0,
        }
        run_mgr.write_manifest(status_counts=status_counts)

        return run_mgr

    def execute_harden(
        self,
        run_mgr: RunManager,
        findings: List[Dict[str, Any]],
    ) -> List[RemediationBundle]:
        """
        Executes Phase 3: Generates structured remediation bundles.
        """
        bundles = []
        for f in findings:
            b = BundleManager.create_bundle(f, cluster_id=f.get("cluster_id"))
            b.write_to_directory(run_mgr.bundles_dir)
            bundles.append(b)

        remediation_md = V6Reporter.render_remediation(bundles)
        run_mgr.write_remediation(remediation_md)
        return bundles

    def execute_apply(
        self,
        run_mgr: RunManager,
        bundles: List[RemediationBundle],
        governor: Optional[PatchGovernor] = None,
    ) -> List[Tuple[str, PatchPolicyDecision]]:
        """
        Executes Phase 4: Evaluates minimal patch governance policies and plans application.
        """
        gov = governor or PatchGovernor()
        decisions = []
        changed_files = set()
        diff_summary_lines = ["# TorusGuard v6 Unified Diff Summary\n"]

        for b in bundles:
            target_f = b.target_files[0] if b.target_files else "app.py"
            decision = gov.evaluate_diff(b.proposed_diff, target_file=target_f)
            decisions.append((b.finding_id, decision))

            if decision.allowed_auto_apply:
                changed_files.update(decision.file_list)
                diff_summary_lines.append(f"## Applied Patch: `{b.finding_id}` (`{target_f}`)")
                diff_summary_lines.append("```diff")
                diff_summary_lines.append(b.proposed_diff.strip())
                diff_summary_lines.append("```\n")

        apply_plan_md = V6Reporter.render_apply_plan(decisions)
        run_mgr.write_apply_plan(apply_plan_md)
        run_mgr.write_diff_summary("\n".join(diff_summary_lines))
        run_mgr.write_changed_files(list(changed_files))

        return decisions

    def execute_recheck(
        self,
        run_mgr: RunManager,
        recheck_scenarios: List[Dict[str, Any]],
    ) -> List[TargetedRecheckResult]:
        """
        Executes Phase 5: Targeted differential rechecks of impacted files.
        """
        results = []
        for sc in recheck_scenarios:
            r = TargetedRechecker.verify_finding(
                finding_id=sc.get("finding_id", "fnd-01"),
                rule_id=sc.get("rule_id", "TG-GENERIC"),
                target_file=sc.get("target_file", "app.py"),
                original_code_snippet=sc.get("orig_snippet", ""),
                post_fix_code_snippet=sc.get("post_snippet", ""),
                is_safe_pattern_present=sc.get("is_safe", True),
                is_unsafe_pattern_present=sc.get("is_unsafe", False),
                introduced_new_flaws=sc.get("regressions"),
                requires_manual_context=sc.get("manual_context", False),
            )
            results.append(r)

        recheck_md = V6Reporter.render_recheck(results)
        run_mgr.write_recheck(recheck_md)

        # Update Manifest counts
        fixed_count = sum(1 for r in results if r.outcome == RecheckOutcome.CONFIRMED_FIXED)
        regressed_count = sum(1 for r in results if r.outcome == RecheckOutcome.REGRESSED)

        run_mgr.write_manifest(
            status_counts={
                "total_findings": len(results),
                "confirmed": 0,
                "high_confidence": 0,
                "needs_review": sum(1 for r in results if r.outcome == RecheckOutcome.NEEDS_MANUAL_REVIEW),
                "remediated": fixed_count,
                "verified_fixed": fixed_count,
                "regressed": regressed_count,
            }
        )

        return results
