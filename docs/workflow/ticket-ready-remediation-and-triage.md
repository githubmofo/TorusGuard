# TorusGuard Ticket-Ready Remediation & Triage Guide

## 🎯 Purpose

This guide explains how engineering teams, security reviewers, and AI coding agents can use TorusGuard reports to triage vulnerabilities, convert findings into issue tickets, apply code patches, and verify closure.

---

## 🚦 1. Triage Workflow by Priority

When reviewing findings in a TorusGuard report, follow this triage order:

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

Every finding card includes a pre-formatted payload:

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

1. **Formulate Bounded Patch:** Run `/torusguard harden` to generate 4-artifact remediation packages strictly adhering to the Ponytail Protocol ($\le 35$ additions, $\le 25$ deletions).
2. **Apply the Patch:** Run `/torusguard apply` to apply the surgical diff directly to repository files with automated rollback backup in `pre_apply/<file>.bak`.
3. **Execute Targeted Recheck:**
   ```bash
   /torusguard recheck
   ```
4. **Assert State:** Verify the finding transitions to **`🟢 Verified Fixed`**, records the post-fix SHA-256 evidence checksum in the audit trail, and exports the updated SARIF report via `/torusguard report`.
