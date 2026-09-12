# TorusGuard Frontend Security & Presentation Architecture

## 1. Overview
The Frontend Architecture document defines TorusGuard's dual relationship with client-side code and user presentation:
1. **Frontend Security Rules:** Guardrails governing client-side web application architectures (React, Next.js, Vite, Vue, Svelte, Angular).
2. **Visual & Terminal Presentation Standards:** Presentation architecture used by TorusGuard to render clean, readable, and actionable security reports in Markdown, 75-column CLI terminals, and standalone HTML dashboards.

---

## 2. The Browser-Code Truth Principle

> **Core Axiom:** If client software receives an artifact, the end-user has uninhibited inspection and modification access to that artifact via browser Developer Tools, network interceptors, or local memory debuggers.

TorusGuard enforces strict frontend boundary rules:
- **`TG-CLIENT-001` (Production Source Maps):** Prevents deployment of unminified `.map` files that expose private business logic and backend route schemas to the public internet.
- **`TG-CLIENT-002` (Sensitive Bundle Content):** Audits frontend build bundles (Vite `dist/`, Next.js `.next/`) to ensure private API keys, payment secret tokens, or internal database URLs (`SUPABASE_SERVICE_ROLE`) are never bundled into client bundles.
- **`TG-DB-001` (Direct Client Database Access):** Forbids client-side JavaScript from executing direct database queries with privileged database credentials.
- **`TG-INPUT-003` (DOM TextContent Reset):** Ensures DOM container clearing uses `.textContent = ''` rather than vulnerable `.innerHTML = ''`.

---

## 3. Standardized 75-Column Terminal Visual Width Engine (`term_ui.py`)

All TorusGuard terminal outputs adhere to a strict visual width of **75 columns**:
- **ANSI Stripping:** Cleans color escape sequences before calculating padding.
- **Unicode Width Math:** Correctly measures double-width emojis (`🛡️`, `✔`, `✖`), zero-width variation selectors (`\ufe0f`), and single-width symbols (`⚠`).
- **Visual Truncation:** Gracefully truncates long file paths and messages with ellipsis (`...`) to preserve rigid box framing.

---

## 4. Visual Single-File HTML Posture Dashboard (`html_reporter.py`)

For executive presentations and compliance sign-offs, `npx torusguard report --html` generates a self-contained, zero-external-CDN dark-mode dashboard:
- **SVG Circular Posture Gauge:** Dynamically animated security health score (0–100).
- **Interactive Closed-Loop Governance Pipeline:** Visual status cards for all 7 lifecycle stages.
- **Unified Diff Viewer:** Syntax-highlighted Before/After comparisons with Ponytail line metrics.
- **Polyglot Ecosystem Badges:** Real-time stack identification cards.

---

## 5. Living Security Report Presentation (`security_report.md`)

The root `security_report.md` provides an immutable ground-truth presentation layer:
- Formatted with standardized 75-column header cards.
- Executive summary table mapping severity to root-cause clusters.
- Real-time Health Score (0–100) reflecting closed and active findings.
- Detailed finding cards with reproducible issue tracker payloads for GitHub, Jira, and Linear.
