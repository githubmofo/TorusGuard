# TorusGuard v0.7.0 Release Notes

**Release Version:** `v0.7.0`  
**Git Tag:** `v0.7.0` (Signed Tag)  
**Release Date:** September 1, 2026  
**Architecture:** Authorized Runtime Validation, Bounded Exploitability Confirmation, Governed Remediation & Targeted Recheck System  

---

## 🎯 Release Decision: APPROVED (YES)

TorusGuard v0.7.0 has successfully concluded all 10 validation phases across 477 automated checks with a **99.6% pass rate (475/477)**. Zero critical security vulnerabilities, zero unhandled exceptions, zero data leaks, and zero safety gate bypasses were detected.

---

## 🚀 What's New in v0.7.0

TorusGuard v0.7.0 extends TorusGuard from a governed static remediation system into an **authorized runtime validation and bounded exploitability confirmation system**:

1. **Target Authorization Gate (`core/authorization.py`):**
   - Enforces signed target ownership or written permission, whitelisted hosts, allowed path prefixes, forbidden paths, and request quotas before any network query is permitted.
   - Emits `authorization.md` and `scope.json`.

2. **Tiered Safety Review Gates (`core/safety_gate.py`):**
   - Implements strict review levels: `Auto-Allowed` (read-only GETs), `Approval Required` (sensitive state-altering actions), and `Manual Only` (permanent block on `/admin/delete`, `/system/shutdown`).

3. **Bounded Exploitability Confirmation (`core/exploit_checker.py`):**
   - Executes safe, passive, single-step verification probes for Auth Bypass, Cross-Tenant IDOR, Header Trust Injection, Path Traversal, and Debug/Config Exposure.
   - Enforces 5 honest statuses: `Runtime Confirmed`, `Runtime Likely`, `Needs Manual Review`, `Not Reproducible in Scope`, and `Blocked by Environment / Controls`.

4. **Web Validation & Secret Redaction (`core/runtime_validator.py`, `core/runtime_evidence.py`):**
   - Performs bounded route crawling with session cookie tracking, injecting transparent `X-TorusGuard-AuthID` audit headers.
   - Automatically sanitizes Bearer tokens, passwords, and API keys prior to logging to `requests.json` and `responses.json`.

5. **Browser-Assisted Verification (`core/browser_verifier.py`):**
   - Verifies client-side route guards and unauthenticated DOM exposure with strict navigation depth limits.

6. **4-Role Multi-Agent Workflow (`core/agent_roles.py`):**
   - Explicit authority separation and handoff contracts between Profiler, Validator, Remediator, and Reviewer roles (`role-audit.json`, `agent-handoffs.md`).

7. **Deterministic Replay Traces (`core/replay_trace.py`):**
   - Serializes verification sequences into replayable, scope-enforced traces (`replay.json`, `replay.md`).

8. **Multi-Analysis SARIF v2.1.0 (`core/sarif.py`):**
   - Partitions static vs runtime findings via `automationDetails.id: torusguard/runtime/` to prevent alert overwrite collisions in GitHub Code Scanning.

---

## 🔍 Scope of Validation

The v0.7.0 release was audited across 8 automated test harnesses covering:
- **10-Phase Runtime Audit (`validate_v0_7_0_runtime.py`):** 67/67 PASS (100%)
- **Hardening & Drift Invariance (`validate_v0_6_3_hardening.py`):** 24/24 PASS (100%)
- **Modern Stack Compatibility (`validate_v0_6_2_modern_stacks.py`):** 19/19 PASS (100%)
- **Scale & Noise Suppression (`validate_v0_6_1_scale.py`):** 22/23 PASS (95.7%)
- **Governed Remediation QA (`validate_qa_v0_6_0.py`):** 93/93 PASS (100%)
- **Core Schemas & Replay (`runner.py`):** 75/75 PASS (100%)
- **End-to-End Multi-Project (`validate_e2e.py`):** 65/65 PASS (100%)
- **Historical Milestone Integrity (`master_validation.py`):** 102/103 PASS (99.0%)

---

## ⚠️ Known Limitations & Out-of-Scope Areas

1. **PatchGovernor Keyword Escalation (Tracked for v0.7.1):**
   - `PatchGovernor.evaluate_diff()` currently checks file paths rather than added diff lines for sensitive keywords (`auth`, `tenant`). Diff lines containing sensitive calls in generic files (`views.py`) require manual flag setting.
2. **Protocol Probing Boundaries:**
   - Runtime exploitability confirmation currently targets HTTP REST APIs. GraphQL and WebSocket runtime probes are scheduled for v0.7.2.
3. **Non-Web Systems:**
   - TorusGuard is built for web applications and APIs; desktop applications, binary payloads, and kernel modules are explicitly out of scope.
4. **Autonomous Pentesting:**
   - TorusGuard is **not** an autonomous offensive penetration testing agent. It does not perform unrestricted fuzzing, memory exploitation, or denial-of-service testing.

---

## 🔐 Artifact Integrity & Checksums

To verify the integrity of release assets, users and CI pipelines can compare the SHA-256 digests against our published `SHA256SUMS` file:

```bash
# Verify checksums
sha256sum -c SHA256SUMS

# Verify GPG signature of release manifest
gpg --verify SHA256SUMS.sig SHA256SUMS
```

All official release git tags are signed by the project maintainer GPG key (`@githubmofo`).
