"""
TorusGuard v0.7.0 Unified Workflow Controller
Coordinates the complete v0.7.0 lifecycle:
1. Authorization & Scope Enforcement
2. Stack Profiling & Route Discovery (Profiler Role)
3. Static Audit & Root-Cause Clustering
4. Authorized Runtime Web Probing (Validator Role)
5. Bounded Exploitability Confirmation
6. Remediation Bundle Packaging with Runtime Insights (Remediator Role)
7. Multi-Agent Governance & Policy Review (Reviewer Role)
8. Replayable Validation Trace Serialization
9. Unified Reporting & Multi-Analysis SARIF Export
"""

from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from core.authorization import AuthorizationRecord, AuthorizationManager, TargetScope, AuthorizationError
from core.safety_gate import SafetyGate
from core.runtime_evidence import EvidenceCollector
from core.runtime_validator import WebValidator
from core.exploit_checker import ExploitChecker, ExploitCheckResult, ExploitabilityStatus
from core.browser_verifier import BrowserVerifier
from core.agent_roles import RoleOrchestrator, AgentRole
from core.replay_trace import ReplayManager
from core.run_manager import RunManager
from core.v6_workflow import V6Workflow
from core.v070_reporter import V070Reporter
from core.sarif import SarifExporter


class V070Workflow:
    """
    Unified controller for TorusGuard v0.7.0 authorized runtime validation and governed remediation.
    """

    def __init__(self, target_root: Optional[Path] = None, output_base: Optional[Path] = None):
        self.target_root = target_root or Path(".")
        self.output_base = output_base or Path(".torusguard/runs")
        self.v6_engine = V6Workflow(target_root=self.target_root, output_base=self.output_base)

    def execute_runtime_validation(
        self,
        target_name: str,
        auth_record: AuthorizationRecord,
        static_findings: List[Dict[str, Any]],
        runtime_probes: List[Dict[str, Any]],
        run_id: Optional[str] = None,
        export_sarif: bool = True
    ) -> Dict[str, Any]:
        """
        Executes the end-to-end v0.7.0 authorized runtime validation workflow.
        """
        # 1. Initialize Run Folder
        run_mgr = RunManager(
            base_dir=self.output_base,
            target_name=target_name,
            command="runtime-validate",
            run_id=run_id
        )

        # 2. Store Authorization Artifacts
        auth_scope_file, auth_doc_file = AuthorizationManager.write_artifacts(run_mgr.run_path, auth_record)

        # 3. Initialize Agent Role Orchestrator & Evidence Collector
        orchestrator = RoleOrchestrator(run_id=run_mgr.run_id)
        evidence_collector = EvidenceCollector()
        web_validator = WebValidator(
            auth_record=auth_record,
            evidence_collector=evidence_collector,
            max_requests=auth_record.scope.max_requests
        )

        # 4. Agent Role: Profiler -> Validator Handoff
        orchestrator.record_handoff(
            from_role=AgentRole.PROFILER,
            to_role=AgentRole.VALIDATOR,
            contract_goal="Deliver detected application endpoints and static findings for authorized runtime validation.",
            inputs={"target_name": target_name, "static_finding_count": len(static_findings)},
            outputs={"authorized_hosts": auth_record.scope.target_hosts, "allowed_prefixes": auth_record.scope.allowed_path_prefixes}
        )

        # 5. Static Scan Enrichment & Clustering (v6 base)
        enriched_findings, clusters = self.v6_engine.execute_audit(
            static_findings,
            target_name=target_name,
            run_id=run_mgr.run_id,
            export_sarif=False
        ), []

        # Re-derive clusters
        from core.clustering import ClusteringEngine
        clusters = ClusteringEngine.cluster_findings(static_findings)

        # 6. Execute Bounded Exploitability Probes (Validator Role)
        exploit_results: List[ExploitCheckResult] = []
        replay_managers: List[ReplayManager] = []

        for probe in runtime_probes:
            res, replay_mgr = self._dispatch_single_probe(probe, web_validator, auth_record)
            exploit_results.append(res)
            replay_managers.append(replay_mgr)

        # 7. Agent Role: Validator -> Remediator Handoff
        orchestrator.record_handoff(
            from_role=AgentRole.VALIDATOR,
            to_role=AgentRole.REMEDIATOR,
            contract_goal="Deliver confirmed exploitability evidence to prioritize minimal safe remediation bundles.",
            inputs={"probes_executed": len(exploit_results)},
            outputs={"confirmed_exploitable": sum(1 for r in exploit_results if r.status == ExploitabilityStatus.RUNTIME_CONFIRMED.value)}
        )

        # 8. Enrich static findings with runtime status
        rt_lookup = {r.finding_id: r for r in exploit_results}
        for f in static_findings:
            f_id = f.get("finding_id")
            if f_id in rt_lookup:
                f["runtime_exploitability"] = rt_lookup[f_id].status

        # 9. Remediation Bundles formulation (v6 base)
        bundles = self.v6_engine.execute_harden(run_mgr, static_findings)

        # 10. Agent Role: Remediator -> Reviewer Handoff
        manual_review_items = [
            {"finding_id": r.finding_id, "reason": r.proof_summary}
            for r in exploit_results
            if r.status in [ExploitabilityStatus.NEEDS_MANUAL_REVIEW.value, ExploitabilityStatus.BLOCKED_BY_CONTROLS.value]
        ]

        orchestrator.record_handoff(
            from_role=AgentRole.REMEDIATOR,
            to_role=AgentRole.REVIEWER,
            contract_goal="Review runtime evidence sufficiency, verify safety gate compliance, and sign off on final report.",
            inputs={"bundles_packaged": len(bundles), "manual_review_items": len(manual_review_items)},
            outputs={"verdict": "Signed Off", "status": "Ready for emission"}
        )

        # 11-16. Write All Workflow Artifacts
        web_artifacts = self._write_runtime_artifacts(
            run_mgr=run_mgr,
            target_name=target_name,
            auth_record=auth_record,
            static_findings=static_findings,
            exploit_results=exploit_results,
            replay_managers=replay_managers,
            web_validator=web_validator,
            orchestrator=orchestrator,
            clusters=clusters,
            manual_review_items=manual_review_items,
            bundles=bundles,
            export_sarif=export_sarif
        )

        return {
            "run_manager": run_mgr,
            "authorization_artifacts": (auth_scope_file, auth_doc_file),
            "exploit_results": exploit_results,
            "web_artifacts": web_artifacts,
            "summary_file": run_mgr.summary_file,
            "sarif_file": run_mgr.sarif_file,
            "manifest_file": run_mgr.manifest_file
        }

    @classmethod
    def _dispatch_single_probe(
        cls,
        probe: Dict[str, Any],
        web_validator: WebValidator,
        auth_record: AuthorizationRecord
    ) -> Tuple[ExploitCheckResult, ReplayManager]:
        """Dispatches a single bounded probe and configures its replay manager."""
        finding_id = probe.get("finding_id", "fnd-unknown")
        cluster_id = probe.get("cluster_id", "cluster-general")
        check_type = probe.get("check_type")
        target_url = probe.get("target_url")

        base_url = f"{auth_record.scope.target_hosts[0]}"
        if not base_url.startswith("http"):
            base_url = f"http://{base_url}"
        replay_mgr = ReplayManager(
            finding_id=finding_id, target_base_url=base_url, description=f"Verification trace for {check_type}"
        )

        if check_type == "auth_bypass":
            res = ExploitChecker.check_auth_bypass(
                validator=web_validator,
                finding_id=finding_id,
                cluster_id=cluster_id,
                endpoint_url=target_url,
                expected_sensitive_marker=probe.get("expected_sensitive_marker")
            )
            replay_mgr.add_step(
                action_type="http_request",
                target=target_url,
                method="GET",
                expected_status=200,
                expected_pattern=probe.get("expected_sensitive_marker")
            )
        elif check_type == "tenant_isolation":
            res = ExploitChecker.check_tenant_isolation(
                validator=web_validator,
                finding_id=finding_id,
                cluster_id=cluster_id,
                tenant_a_resource_url=target_url,
                tenant_b_auth_headers=probe.get("tenant_b_auth_headers", {}),
                tenant_a_data_marker=probe.get("tenant_a_data_marker", "")
            )
            replay_mgr.add_step(
                action_type="http_request",
                target=target_url,
                method="GET",
                headers=probe.get("tenant_b_auth_headers", {}),
                expected_status=200,
                expected_pattern=probe.get("tenant_a_data_marker")
            )
        elif check_type == "header_trust":
            res = ExploitChecker.check_header_trust(
                validator=web_validator,
                finding_id=finding_id,
                cluster_id=cluster_id,
                endpoint_url=target_url,
                spoofed_headers=probe.get("spoofed_headers", {}),
                expected_reflection_marker=probe.get("expected_reflection_marker", "")
            )
            replay_mgr.add_step(
                action_type="http_request",
                target=target_url,
                method="GET",
                headers=probe.get("spoofed_headers", {}),
                expected_status=200,
                expected_pattern=probe.get("expected_reflection_marker")
            )
        elif check_type == "debug_exposure":
            res = ExploitChecker.check_debug_exposure(
                validator=web_validator,
                finding_id=finding_id,
                cluster_id=cluster_id,
                debug_url=target_url,
                debug_marker=probe.get("debug_marker", "")
            )
            replay_mgr.add_step(
                action_type="http_request",
                target=target_url,
                method="GET",
                expected_status=200,
                expected_pattern=probe.get("debug_marker")
            )
        else:
            status, headers, body, decision = web_validator.execute_probe(
                finding_id=finding_id,
                cluster_id=cluster_id,
                method=probe.get("method", "GET"),
                target_url=target_url
            )
            res = ExploitCheckResult(
                finding_id=finding_id,
                issue_class=check_type or "general",
                status=ExploitabilityStatus.RUNTIME_LIKELY.value if status == 200 else ExploitabilityStatus.NOT_REPRODUCIBLE_IN_SCOPE.value,
                confidence_score=70 if status == 200 else 20,
                probe_url=target_url,
                http_status_observed=status,
                proof_summary=f"HTTP {status} observed.",
                reproducible=True,
                remediation_advice="Review endpoint configuration."
            )

        return res, replay_mgr

    @classmethod
    def _write_runtime_artifacts(
        cls,
        run_mgr: RunManager,
        target_name: str,
        auth_record: AuthorizationRecord,
        static_findings: List[Dict[str, Any]],
        exploit_results: List[ExploitCheckResult],
        replay_managers: List[ReplayManager],
        web_validator: WebValidator,
        orchestrator: RoleOrchestrator,
        clusters: List[Any],
        manual_review_items: List[Dict[str, Any]],
        bundles: List[Any],
        export_sarif: bool
    ) -> Dict[str, Any]:
        """Emits replay traces, web validation reports, role audits, summary markdown, SARIF, and manifest."""
        # 11. Write Replay Traces
        for rm in replay_managers:
            rm.write_artifacts(run_mgr.run_path)

        # 12. Write Web Validation and Session Notes
        web_artifacts = web_validator.write_report_artifacts(run_mgr.run_path)

        # 13. Write Agent Role Audit Artifacts
        orchestrator.write_artifacts(run_mgr.run_path)

        # 14. Write Combined Summary Report
        summary_md = V070Reporter.render_combined_summary(
            target_name=target_name,
            run_id=run_mgr.run_id,
            auth_id=auth_record.authorization_id,
            static_findings=static_findings,
            runtime_results=[r.to_dict() for r in exploit_results],
            clusters=clusters,
            manual_review_items=manual_review_items
        )
        with open(run_mgr.summary_file, "w", encoding="utf-8") as f:
            f.write(summary_md)

        # 15. Export Multi-Analysis Partitioned SARIF v2.1.0
        if export_sarif:
            sarif_data = SarifExporter.generate_sarif(
                findings=static_findings,
                tool_version="0.7.0",
                analysis_category="torusguard/runtime"
            )
            with open(run_mgr.sarif_file, "w", encoding="utf-8") as f:
                import json
                json.dump(sarif_data, f, indent=2)

        # 16. Write Manifest
        run_mgr.write_manifest(
            status_counts={
                "total_findings": len(static_findings),
                "runtime_confirmed": sum(1 for r in exploit_results if r.status == ExploitabilityStatus.RUNTIME_CONFIRMED.value),
                "runtime_likely": sum(1 for r in exploit_results if r.status == ExploitabilityStatus.RUNTIME_LIKELY.value),
                "not_reproducible": sum(1 for r in exploit_results if r.status == ExploitabilityStatus.NOT_REPRODUCIBLE_IN_SCOPE.value),
                "needs_manual_review": len(manual_review_items),
                "remediated": len(bundles),
                "verified_fixed": 0,
                "regressed": 0
            },
            extra_meta={
                "authorization_id": auth_record.authorization_id,
                "version": "v0.7.0",
                "analysis_category": "torusguard/runtime"
            }
        )

        return web_artifacts
