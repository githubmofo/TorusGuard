# TorusGuard Ticket-Ready Remediation & Triage Guide

## 🎯 Purpose

This guide explains how engineering teams, security reviewers, and AI coding agents can use TorusGuard reports to triage vulnerabilities, convert findings into issue tickets, apply code patches, and verify closure using both Terminal CLI commands and AI Agent Chat slash commands.

---

## 🚦 1. Triage Workflow by Priority

When reviewing findings in `security_report.md` or an audit report, follow this triage order:

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

Every finding card in `security_report.md` and audit run manifests includes an issue tracker payload:

1. Copy the markdown content from the finding card.
2. Paste directly into your team's issue tracker (GitHub Issue, Jira Story, or Linear Issue).

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
Run `npx torusguard recheck` or `/torusguard recheck` to verify resolution.
```

---

## 🔁 3. Remediation & Closure Verification

1. **Formulate Bounded Patch:** Run `npx torusguard harden` (or `/torusguard harden`) to generate surgical remediation packages strictly adhering to the Ponytail Protocol ($\le 35$ additions, $\le 25$ deletions).
2. **Apply the Patch:** Run `npx torusguard apply [--yes]` (or `/torusguard apply`) to apply surgical diffs with automated pre-apply rollback backups in `.torusguard/snapshots/<run_id>/`.
3. **Execute Targeted Recheck:**
   ```bash
   # Terminal CLI
   npx torusguard recheck

   # AI Agent Chat
   /torusguard recheck
   ```
4. **Living Security Report Closure:** Once `recheck` confirms resolution, `security_report.md` marks the finding as `RESOLVED 🟢` and updates the workspace Health Score (0–100). The fix is distilled into a Golden Fix Recipe in `.torusguard/memory/patterns.json`.
