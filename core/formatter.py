"""
TorusGuard Report Formatter (v0.5.1)
Renders canonical findings with provenance tracking, auditable confidence scoring, and explicit retest records.
"""

from typing import Dict, Any, List
from .models import (
    AuditReport,
    Finding,
    SeverityLevel,
    ConfidenceBand,
    FindingStatus,
)


class ReportFormatter:
    """
    Produces deterministic, human-readable Markdown and structured JSON audit reports.
    """

    SEVERITY_BADGES = {
        SeverityLevel.CRITICAL: "🔴 Critical",
        SeverityLevel.HIGH: "🟠 High",
        SeverityLevel.MEDIUM: "🟡 Medium",
        SeverityLevel.LOW: "🔵 Low",
        SeverityLevel.INFORMATIONAL: "ℹ️ Info",
    }

    CONFIDENCE_BADGES = {
        ConfidenceBand.CONFIRMED: "🔒 Confirmed",
        ConfidenceBand.HIGH_CONFIDENCE: "🟢 High Confidence",
        ConfidenceBand.MEDIUM_CONFIDENCE: "🟡 Medium Confidence",
        ConfidenceBand.LOW_CONFIDENCE: "🟠 Low Confidence",
        ConfidenceBand.UNCONFIRMED: "⚪ Unconfirmed",
        ConfidenceBand.NEEDS_REVIEW: "🔍 Needs Review",
        ConfidenceBand.INFORMATIONAL: "ℹ️ Informational",
        ConfidenceBand.NOT_APPLICABLE: "⚪ N/A",
    }

    STATUS_BADGES = {
        FindingStatus.CONFIRMED: "🔴 Confirmed",
        FindingStatus.HIGH_CONFIDENCE: "🟠 High Confidence",
        FindingStatus.MEDIUM_CONFIDENCE: "🟡 Medium Confidence",
        FindingStatus.LOW_CONFIDENCE: "⚪ Low Confidence",
        FindingStatus.UNCONFIRMED: "⚪ Unconfirmed",
        FindingStatus.NEEDS_REVIEW: "🔍 Needs Review",
        FindingStatus.REMEDIATED: "🟡 Remediated (Pending Retest)",
        FindingStatus.VERIFIED_FIXED: "🟢 Verified Fixed",
        FindingStatus.SUPPRESSED: "⚪ Suppressed",
    }

    @staticmethod
    def render_markdown(report: AuditReport) -> str:
        report.calculate_summary()
        summary = report.summary_counts

        # Overall posture indicator
        if summary.get("critical", 0) > 0 or summary.get("high", 0) > 0:
            posture_icon = "🔴 Action Required"
        elif summary.get("medium", 0) > 0:
            posture_icon = "🟡 Warnings Found"
        elif summary.get("needs_review", 0) > 0:
            posture_icon = "🔍 Needs Review"
        else:
            posture_icon = "🟢 Ready / Verified Safe"

        lines = [
            f"# TorusGuard Security Audit & Provenance Report",
            f"",
            f"> **Engine Version:** TorusGuard `{report.torusguard_version}` (Provenance & Auditable Confidence Release)  ",
            f"> **Generated At:** `{report.generated_at}`  ",
            f"> **Overall Posture:** **{posture_icon}** | **Average Confidence:** `{summary.get('average_confidence_score', 0)}/100`",
            f"",
            f"---",
            f"",
            f"## 🔍 Detected Stack",
            f"- **Project Name:** `{report.project_name}`",
            f"- **Primary Language:** `{report.detected_stack.get('language', 'Unknown')}`",
            f"- **Framework:** `{report.detected_stack.get('framework', 'Unknown')}`",
            f"- **Data Layer:** `{report.detected_stack.get('data_layer', 'None')}`",
            f"- **Dependency Files:** `{report.detected_stack.get('dependency_files', 'None')}`",
            f"- **Detection Evidence:** `{report.detected_stack.get('detection_evidence', 'N/A')}`",
            f"- **Detection Confidence:** `{report.detected_stack.get('confidence', 'Confirmed')}`",
            f"",
            f"---",
            f"",
            f"## 📊 Executive Summary & Metrics",
            f"",
            f"| Metric | Count | Description |",
            f"|---|:---:|---|",
            f"| **Total Findings** | `{summary.get('total_findings', 0)}` | Total normalized security findings tracked |",
            f"| **Critical / High** | `{summary.get('critical', 0) + summary.get('high', 0)}` | Severe findings requiring immediate remediation |",
            f"| **Confirmed (90–100 Score)** | `{summary.get('confirmed', 0)}` | Proven with deterministic source/runtime evidence |",
            f"| **High Confidence (70–89)** | `{summary.get('high_confidence', 0)}` | Strong indicators present; localized verification recommended |",
            f"| **Needs Review / Unconfirmed** | `{summary.get('needs_review', 0)}` | Out-of-band context requires human architectural review |",
            f"| **Verified Fixed** | `{summary.get('verified_fixed', 0)}` | Successfully verified fixed via post-remediation retest |",
            f"",
            f"---",
            f"",
            f"## 🛡️ Findings with Provenance & Evidence Packages",
            f"",
        ]

        if not report.findings:
            lines.append("🎉 **No vulnerabilities detected!** Application complies with all TorusGuard security baselines.\n")
        else:
            for idx, f in enumerate(report.findings, 1):
                sev_badge = ReportFormatter.SEVERITY_BADGES.get(f.severity.level, str(f.severity.level))
                conf_badge = ReportFormatter.CONFIDENCE_BADGES.get(f.confidence.band, str(f.confidence.band))
                status_badge = ReportFormatter.STATUS_BADGES.get(f.status, str(f.status.value))
                loc_str = f"{f.affected_component.target_path}"
                if f.affected_component.start_line:
                    loc_str += f":{f.affected_component.start_line}"
                if f.affected_component.symbol:
                    loc_str += f" (`{f.affected_component.symbol}`)"

                factors = f.confidence.factors

                lines.extend([
                    f"### {idx}. [{f.rule_id}] {f.title}",
                    f"",
                    f"- **Finding ID:** `{f.finding_id}`",
                    f"- **Severity:** {sev_badge} | **Status:** {status_badge}",
                    f"- **Auditable Confidence:** {conf_badge} (`{f.confidence.score}/100`)",
                    f"- **Category:** `{f.category.value}`",
                    f"- **Location:** `{loc_str}`",
                    f"- **Lifecycle Stage:** `{f.lifecycle_stage.value}`",
                ])

                # Standards mapping
                reqs = []
                if f.asvs_control:
                    reqs.append(f"OWASP ASVS: `{f.asvs_control}`")
                if f.cwe:
                    reqs.append(f"CWE: `{f.cwe}`")
                if f.nist_ssdf:
                    reqs.append(f"NIST SSDF: `{f.nist_ssdf}`")
                if reqs:
                    lines.append(f"- **Requirement Mapping:** {', '.join(reqs)}")

                lines.extend([
                    f"",
                    f"#### 🔍 Auditable Confidence Score Breakdown (`{f.confidence.score}/100`)",
                    f"- **Evidence Quality:** `{factors.evidence_quality}/35` pts (Direct source AST/syntax match)",
                    f"- **Reproduction Success:** `{factors.reproduction_success}/25` pts (Deterministic reproduction path)",
                    f"- **Independent Confirmations:** `{factors.independent_confirmations}/15` pts (Corroborated across files)",
                    f"- **Environmental Clarity:** `{factors.environmental_clarity}/15` pts (No ambiguous out-of-band proxy/service)",
                    f"- **Manual Review Status:** `{factors.manual_review_status}/10` pts (Reviewer validation)",
                    f"- **Confidence Rationale:** {f.confidence.rationale}",
                    f"",
                    f"#### 🔗 Provenance Chain",
                    f"- **Discovery Module:** `{f.provenance.discovery_module}`",
                    f"- **Triggering Input:** `{f.provenance.triggering_input}`",
                    f"- **Decision Path:**",
                ])

                for step in f.provenance.decision_path:
                    lines.append(f"  1. {step}")

                lines.extend([
                    f"- **Verification Step:** {f.provenance.verification_step}",
                    f"",
                    f"#### 📦 Raw Technical Evidence Package",
                ])

                for ev_idx, ev in enumerate(f.evidence, 1):
                    lines.extend([
                        f"**Evidence Item #{ev_idx} ({ev.type.value}):** `{ev.location}`",
                        f"- **SHA-256 Checksum:** `{ev.sha256_checksum}`",
                        f"- **Rationale:** {ev.rationale}",
                        f"```",
                        f"{ev.raw_snippet.strip()}",
                        f"```",
                    ])

                lines.extend([
                    f"#### 🧠 Analysis & Risk Rationale",
                    f"- **Raw Facts Summary:** {f.notes.raw_facts_summary}",
                    f"- **AI Risk Interpretation:** {f.notes.ai_interpretation}",
                    f"- **Severity Rubric Justification:** {f.severity.rubric_justification}",
                    f"",
                    f"#### 🛠️ Prescriptive Remediation",
                    f"**Problem Statement:** {f.remediation.problem_statement}",
                    f"",
                    f"**Action:** {f.remediation.recommended_fix}",
                    f"",
                    f"**Code Pattern ({f.remediation.framework_pattern.framework}):**",
                    f"```diff",
                    f"- // UNSAFE ORIGINAL",
                    f"- {f.remediation.framework_pattern.unsafe_snippet.strip()}",
                    f"+ // SAFE REMEDIATION",
                    f"+ {f.remediation.framework_pattern.safe_snippet.strip()}",
                    f"```",
                    f"",
                    f"**Verification Method:** {f.remediation.verification_method}",
                    f"",
                    f"**Residual Risk Notes:** {f.remediation.residual_risk_notes}",
                    f"",
                    f"#### 🔁 Retest & Closure Status",
                ])

                if f.retest_result.retest_performed:
                    lines.extend([
                        f"- **Retest Executed:** ✅ Yes (`{f.retest_result.retest_timestamp}`)",
                        f"- **Closure Status:** **`{f.retest_result.closure_status.value}`**",
                        f"- **Retest Method:** `{f.retest_result.retest_method}`",
                        f"- **Post-Fix Evidence Hash:** `{f.retest_result.retest_evidence_hash}`",
                        f"- **Verifier Notes:** {f.retest_result.verifier_notes}",
                    ])
                else:
                    lines.extend([
                        f"- **Retest Executed:** ⏳ Pending (Run `/torusguard recheck` after applying fix)",
                        f"- **Closure Status:** `{f.status.value}`",
                    ])

                lines.extend([
                    f"",
                    f"---",
                    f"",
                ])

        lines.extend([
            f"## 📋 Verification & Next Steps",
            f"1. **Apply Framework Patches:** Follow the Before/After remediation diffs above.",
            f"2. **Execute Retest:** Run `/torusguard recheck` to verify that findings transition to `Verified Fixed`.",
            f"3. **Inspect Needs Review Items:** Verify service layers, reverse proxy headers, and cloud IAM permissions.",
            f"",
            f"---",
            f"",
            f"## ⚖️ Technical Boundaries & Integrity",
            f"TorusGuard is an open-source Markdown-first security guidance framework. It is not an automated binary scanner or penetration-testing replacement. Raw code evidence hashes provide verifiable provenance, but human architectural review is required for complex domain workflows.",
        ])

        return "\n".join(lines)
