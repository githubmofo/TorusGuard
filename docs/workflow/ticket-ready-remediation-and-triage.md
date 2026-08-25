# TorusGuard Ticket-Ready Remediation & Triage Guide

## 🎯 Purpose

This guide explains how engineering teams, security reviewers, and AI coding agents can use TorusGuard v0.5.4 reports to triage vulnerabilities, convert findings into issue tickets, apply code patches, and verify closure.

---

## 🚦 1. Triage Workflow by Priority

When reviewing Section 5 of a TorusGuard report, follow this triage order:

```text
┌────────────────────────────────────────┐
│ 🚨 Immediate Priority (P0)             │ ──► Halt deployment / apply fix immediately
├────────────────────────────────────────┤
│ 🟠 Near-Term Priority (P1)             │ ──► Schedule into current sprint work
├────────────────────────────────────────┤
│ 🟡 Backlog / Hardening (P2)            │ ──► Add to security hardening backlog
└────────────────────────────────────────┘
```

---

## 🎫 2. Creating Issue Tracker Tickets (GitHub / Jira / Linear)

Every finding in Section 4 includes a pre-formatted payload:

1. Click on the expandable `<details>` section: **🎫 Copy-Paste Issue Tracker Payload**.
2. Copy the markdown content.
3. Paste directly into your team's issue tracker (GitHub Issue, Jira Story, or Linear Issue).

### Example Issue Payload
```markdown
### [Security] Fix TG-AUTH-007: Missing Property-Level Authorization

**Priority:** 🚨 Immediate (P0) | **Severity:** 🔴 Critical | **Location:** `app/views.py:45`

#### Problem
Invoice records are fetched by ID without verifying that the requesting user owns the invoice.

#### Business Impact
Unauthorized users can access financial records and private customer invoices across organization boundaries.

#### Proposed Fix
Filter querysets by authenticated user ownership: `Invoice.objects.filter(owner=request.user)`.

#### Verification
Run `/torusguard recheck` to verify resolution.
```

---

## 🔁 3. Remediation & Closure Verification

1. **Apply the Patch:** Follow the Before/After diff provided in the detailed finding block.
2. **Execute Retest:**
   ```bash
   /torusguard recheck
   ```
3. **Verify Status Transition:** The finding will transition to **`🟢 Verified Fixed`** and record the post-fix SHA-256 evidence checksum in the audit trail.
