"""
TorusGuard Report Formatter (v0.5.4)
Renders comprehensive, actionable, ticket-ready Markdown and structured JSON audit reports.
"""

from typing import Dict, Any, List
from .models import (
    AuditReport,
    Finding,
    SeverityLevel,
    ConfidenceBand,
    FindingStatus,
    RemediationPriority,
)


class ReportFormatter:
    """
    Produces deterministic, human-readable, ticket-ready Markdown and structured JSON audit reports.
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

    PRIORITY_BADGES = {
        RemediationPriority.IMMEDIATE: "🚨 Immediate (P0)",
        RemediationPriority.NEAR_TERM: "🟠 Near-Term (P1)",
        RemediationPriority.BACKLOG: "🟡 Backlog (P2)",
    }

    @staticmethod
    def render_markdown(report: AuditReport) -> str:
        report.calculate_summary()
        summary = report.summary_counts

        # Overall posture indicator
        if summary.get("critical", 0) > 0 or summary.get("high", 0) > 0:
            posture_icon = "🔴 Action Required (Pre-Deployment Blockers Found)"
        elif summary.get("medium", 0) > 0:
            posture_icon = "🟡 Warnings Found (Hardening Recommended)"
        elif summary.get("needs_review", 0) > 0:
            posture_icon = "🔍 Needs Review (Architectural Verification Required)"
        else:
            posture_icon = "🟢 Ready / Verified Safe (All Checks Passing)"

        lines = [
            f"# TorusGuard Security Audit & Remediation Report",
            f"",
            f"> **Project:** `{report.project_name}` | **Repository Reference:** `{report.repository_ref}`  ",
            f"> **Engine Version:** TorusGuard `{report.torusguard_version}` (Actionable Remediation & Usability Release)  ",
            f"> **Generated At:** `{report.generated_at}` | **Report Owner:** `{report.report_owner}`  ",
            f"> **Overall Security Posture:** **{posture_icon}**",
            f"",
            f"---",
            f"",
            f"## 1. 📋 Executive Summary",
            f"",
            f"This security assessment evaluated **{report.project_name}** using TorusGuard's evidence-backed finding lifecycle and deterministic validation engine. The scan analyzed source files, configuration manifests, data queries, and API endpoint boundaries.",
            f"",
            f"- **Key Risk Themes:** " + (
                "Critical authorization boundaries, input handling, and configuration exposures require remediation."
                if summary.get("critical", 0) > 0 or summary.get("high", 0) > 0
                else "No high-severity vulnerabilities detected; defensive baselines satisfied."
            ),
            f"- **Validation Status:** `{summary.get('confirmed', 0)}` Confirmed Findings | `{summary.get('needs_review', 0)}` Needs Review | `{summary.get('verified_fixed', 0)}` Verified Fixed",
            f"- **Immediate Action Required:** " + (
                f"Triage and remediate `{summary.get('immediate_priority', 0)}` P0 immediate priority finding(s) before production deployment."
                if summary.get("immediate_priority", 0) > 0
                else "Application meets primary security release criteria."
            ),
            f"",
            f"### 📊 Security Metrics at a Glance",
            f"",
            f"| Metric | Count | Stakeholder Guidance |",
            f"|---|:---:|---|",
            f"| **Total Tracked Findings** | `{summary.get('total_findings', 0)}` | Total normalized finding objects |",
            f"| **Immediate Priority (P0)** | `{summary.get('immediate_priority', 0)}` | 🚨 Pre-deployment blockers |",
            f"| **Near-Term Priority (P1)** | `{summary.get('near_term_priority', 0)}` | 🟠 Current sprint patch cycle |",
            f"| **Backlog / Hardening (P2)** | `{summary.get('backlog_priority', 0)}` | 🟡 Defense-in-depth backlog |",
            f"| **Auditable Average Confidence** | `{summary.get('average_confidence_score', 0)}/100` | Mathematical evidence score |",
            f"| **Verified Fixed Post-Retest** | `{summary.get('verified_fixed', 0)}` | 🟢 Retest confirmed resolution |",
            f"",
            f"---",
            f"",
            f"## 2. 🔍 Scope and Methodology",
            f"",
            f"- **Target Application:** `{report.project_name}`",
            f"- **Detected Stack:** `{report.detected_stack.get('language', 'Unknown')}` / `{report.detected_stack.get('framework', 'Unknown')}` (Data layer: `{report.detected_stack.get('data_layer', 'None')}`)",
            f"- **Tested Scope:** Source code AST structures, route handlers, serializer definitions, database queries, upload paths, and environment configurations.",
            f"- **Out of Scope:** Live production network penetration testing, active DDoS simulation, third-party SaaS infrastructure compliance audits.",
            f"- **Interpretation Guide:** Every finding is backed by immutable cryptographic evidence hashes. Findings marked `Needs Review` reflect out-of-band architecture requiring human architectural verification.",
            f"",
            f"---",
            f"",
            f"## 3. 📑 Key Findings Summary Table",
            f"",
            f"| Ref ID | Title | Category | Severity | Confidence | Status | Priority | Location |",
            f"|---|---|---|:---:|:---:|:---:|:---:|---|",
        ]

        if not report.findings:
            lines.append("| — | *No findings identified* | — | — | — | 🟢 Safe | — | — |")
        else:
            for f in report.findings:
                sev_badge = ReportFormatter.SEVERITY_BADGES.get(f.severity.level, str(f.severity.level))
                conf_badge = f"{f.confidence.score}/100"
                stat_badge = ReportFormatter.STATUS_BADGES.get(f.status, str(f.status.value))
                pri_badge = ReportFormatter.PRIORITY_BADGES.get(f.remediation_priority, str(f.remediation_priority))
                loc_str = f"`{f.affected_component.target_path}`"
                if f.affected_component.start_line:
                    loc_str += f":{f.affected_component.start_line}"
                lines.append(
                    f"| `{f.rule_id}` | **{f.title}** | `{f.category.value}` | {sev_badge} | {conf_badge} | {stat_badge} | {pri_badge} | {loc_str} |"
                )

        lines.extend([
            f"",
            f"---",
            f"",
            f"## 4. 🛡️ Detailed Findings",
            f"",
        ])

        if not report.findings:
            lines.append("🎉 **No vulnerabilities detected!** Application complies with all TorusGuard security baselines.\n")
        else:
            for idx, f in enumerate(report.findings, 1):
                sev_badge = ReportFormatter.SEVERITY_BADGES.get(f.severity.level, str(f.severity.level))
                conf_badge = ReportFormatter.CONFIDENCE_BADGES.get(f.confidence.band, str(f.confidence.band))
                status_badge = ReportFormatter.STATUS_BADGES.get(f.status, str(f.status.value))
                pri_badge = ReportFormatter.PRIORITY_BADGES.get(f.remediation_priority, str(f.remediation_priority))

                loc_str = f"{f.affected_component.target_path}"
                if f.affected_component.start_line:
                    loc_str += f":{f.affected_component.start_line}"
                if f.affected_component.symbol:
                    loc_str += f" (`{f.affected_component.symbol}`)"

                factors = f.confidence.factors

                lines.extend([
                    f"### {idx}. [{f.rule_id}] {f.title}",
                    f"",
                    f"> **Finding ID:** `{f.finding_id}` | **Remediation Priority:** **{pri_badge}**  ",
                    f"> **Severity:** {sev_badge} | **Auditable Confidence:** {conf_badge} (`{f.confidence.score}/100`) | **Status:** {status_badge}  ",
                    f"> **Location:** `{loc_str}` | **Lifecycle Stage:** `{f.lifecycle_stage.value}`",
                    f"",
                    f"#### 🏢 Business Impact & Executive Context",
                    f"{f.notes.business_impact}",
                    f"",
                    f"#### ⚙️ Technical Mechanics & Threat Context",
                    f"{f.notes.technical_description}",
                    f"",
                    f"#### 🔍 Auditable Confidence Score Breakdown (`{f.confidence.score}/100`)",
                    f"- **Evidence Quality:** `{factors.evidence_quality}/35` pts (Direct source AST/syntax match)",
                    f"- **Reproduction Success:** `{factors.reproduction_success}/25` pts (Deterministic reproduction path)",
                    f"- **Independent Confirmations:** `{factors.independent_confirmations}/15` pts (Corroborated across files)",
                    f"- **Environmental Clarity:** `{factors.environmental_clarity}/15` pts (No ambiguous out-of-band proxy/service)",
                    f"- **Manual Review Status:** `{factors.manual_review_status}/10` pts (Reviewer validation)",
                    f"- **Confidence Justification:** {f.confidence.rationale}",
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
                    f"#### 📦 Technical Evidence Package",
                ])

                for ev_idx, ev in enumerate(f.evidence, 1):
                    lines.extend([
                        f"**Evidence Item #{ev_idx} ({ev.type.value}):** `{ev.location}`",
                        f"- **SHA-256 Checksum:** `{ev.sha256_checksum}`",
                        f"- **Rationale:** {ev.rationale}",
                        f"```",
                        f"{ev.get_masked_snippet().strip()}",
                        f"```",
                    ])

                lines.extend([
                    f"#### 🛠️ Prescriptive Remediation",
                    f"**Problem Statement:** {f.remediation.problem_statement}",
                    f"",
                    f"**Recommended Action:** {f.remediation.recommended_fix}",
                    f"",
                    f"**Framework Patch ({f.remediation.framework_pattern.framework}):**",
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

                # Copy-pasteable Ticket/Issue payload
                lines.extend([
                    f"",
                    f"<details>",
                    f"<summary>🎫 Copy-Paste Issue Tracker Payload (GitHub / Jira / Linear)</summary>",
                    f"",
                    f"```markdown",
                    f"### [Security] Fix {f.rule_id}: {f.title}",
                    f"",
                    f"**Priority:** {pri_badge} | **Severity:** {sev_badge} | **Location:** `{loc_str}`",
                    f"",
                    f"#### Problem",
                    f"{f.remediation.problem_statement}",
                    f"",
                    f"#### Business Impact",
                    f"{f.notes.business_impact}",
                    f"",
                    f"#### Proposed Fix",
                    f"{f.remediation.recommended_fix}",
                    f"",
                    f"#### Verification",
                    f"Run `/torusguard recheck` to verify resolution.",
                    f"```",
                    f"</details>",
                    f"",
                    f"---",
                    f"",
                ])

        # Section 5: Remediation Priorities
        lines.extend([
            f"## 5. 🎯 Remediation Priorities & Triage Roadmap",
            f"",
            f"### 🚨 Immediate Priority (P0 — Pre-Deployment Blockers)",
        ])

        immediate_findings = [f for f in report.findings if f.remediation_priority == RemediationPriority.IMMEDIATE]
        if immediate_findings:
            for f in immediate_findings:
                lines.append(f"- [ ] **[{f.rule_id}] {f.title}** (`{f.affected_component.target_path}`) — {f.remediation.recommended_fix}")
        else:
            lines.append("- *No immediate P0 blockers.*")

        lines.extend([
            f"",
            f"### 🟠 Near-Term Priority (P1 — Current Sprint Patch Cycle)",
        ])

        near_term_findings = [f for f in report.findings if f.remediation_priority == RemediationPriority.NEAR_TERM]
        if near_term_findings:
            for f in near_term_findings:
                lines.append(f"- [ ] **[{f.rule_id}] {f.title}** (`{f.affected_component.target_path}`) — {f.remediation.recommended_fix}")
        else:
            lines.append("- *No near-term P1 items.*")

        lines.extend([
            f"",
            f"### 🟡 Backlog / Hardening (P2 — Defense-in-Depth)",
        ])

        backlog_findings = [f for f in report.findings if f.remediation_priority == RemediationPriority.BACKLOG]
        if backlog_findings:
            for f in backlog_findings:
                lines.append(f"- [ ] **[{f.rule_id}] {f.title}** (`{f.affected_component.target_path}`) — {f.remediation.recommended_fix}")
        else:
            lines.append("- *No backlog hardening items.*")

        # Section 6: Retest & Verification
        lines.extend([
            f"",
            f"---",
            f"",
            f"## 6. 🔁 Retest & Verification Workflow",
            f"1. **Apply Code Patches:** Follow the Before/After framework diffs provided in Section 4.",
            f"2. **Execute Retest:** Run `/torusguard recheck` to verify that findings transition to `Verified Fixed`.",
            f"3. **Inspect Needs Review Items:** For items marked `Needs Review`, manually verify service-layer authorization and cloud IAM policies.",
            f"",
            f"---",
            f"",
            f"## 7. ⚖️ Limitations & Operational Boundaries",
            f"- **Source-Only Analysis:** Findings are derived from static source code inspection, AST patterns, and configuration files.",
            f"- **Manual Review Boundary:** When authorization or validation is delegated to out-of-band microservices, reverse proxies, or cloud IAM, TorusGuard assigns `Needs Review`.",
            f"- **Sensitive Data Masking:** All secrets, tokens, and credentials in evidence snippets are automatically redacted.",
            f"",
            f"---",
            f"",
            f"## 8. 📚 Appendix & Reference Models",
            f"",
            f"### Confidence Scoring Model (0–100)",
            f"- **90–100 (`Confirmed`):** Direct, indisputable proof of vulnerability with reachable sink.",
            f"- **70–89 (`High Confidence`):** Strong static indicators present; localized verification recommended.",
            f"- **50–69 (`Medium Confidence`):** Probable flaw; runtime confirmation recommended.",
            f"- **< 50 (`Needs Review`):** Insufficient evidence or out-of-band architectural delegation.",
            f"",
            f"### Severity Rubric",
            f"- **Critical (P0):** Remote Code Execution, unauthenticated SQL injection, hardcoded secrets, complete auth bypass.",
            f"- **High (P1):** Object-level authorization bypass (IDOR), SSRF, XSS, tenant data leakage.",
            f"- **Medium (P2):** Missing rate limits, insecure cookie attributes, missing CSRF tokens.",
            f"- **Low / Info:** Verbose error banners, public source maps, hardening recommendations.",
        ])

        return "\n".join(lines)
