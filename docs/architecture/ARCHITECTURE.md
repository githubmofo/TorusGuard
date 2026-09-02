# TorusGuard System Architecture

## Table of Contents
1. [System Overview](#1-system-overview)
2. [Design Principles](#2-design-principles)
3. [High-Level Architecture](#3-high-level-architecture)
4. [System Context](#4-system-context)
5. [Layered Architecture](#5-layered-architecture)
6. [Component Architecture](#6-component-architecture)
7. [Request Lifecycle](#7-request-lifecycle)
8. [Data Flow Architecture](#8-data-flow-architecture)
9. [Technology Stack](#9-technology-stack)
10. [Non-Functional Requirements](#10-non-functional-requirements)
11. [Cross-Cutting Concerns](#11-cross-cutting-concerns)
12. [Module Dependency Map](#12-module-dependency-map)
13. [Integration Points](#13-integration-points)
14. [Scalability Strategy](#14-scalability-strategy)
15. [Failure Handling & Resilience](#15-failure-handling--resilience)

---

## 1. System Overview

**TorusGuard** is a Markdown-first, portable security verification skill and automated analysis workflow engine designed for AI coding agents and full-stack software engineers.

TorusGuard addresses the emerging risk profile created by AI-assisted software development: while AI agents rapidly generate functional application code, they frequently overlook foundational security boundaries—such as client-side database credentials, unescaped template directives, missing tenant isolation, unvalidated redirect/SSRF paths, and missing authorization decorators.

TorusGuard acts as an autonomous, deterministic security co-pilot. It operates directly within developer IDEs, AI coding assistants (e.g., Cursor, Antigravity, Claude Code, Cline, Codex, Gemini CLI), and continuous integration pipelines without requiring external server daemons or cloud SaaS dependencies.

---

## 2. Design Principles

TorusGuard is built upon six foundational engineering tenets:

1. **The Browser-Code Truth:** Any code, state, or secret transmitted to a client browser can and will be inspected via DevTools. All authorization, tenant isolation, and credential handling must reside strictly on trusted server runtimes.
2. **Markdown-First & Agent-Portable:** Architecture and rules are defined as standard Markdown documents with YAML frontmatter, making them immediately consumable by both human engineers and LLM reasoning loops.
3. **Deterministic Finding Lifecycle:** Security findings transition through a formal 7-stage closed-loop state machine (`Detect` ──► `Classify` ──► `Verify` ──► `Remediate` ──► `Apply` ──► `Re-check` ──► `Archive`).
4. **Least-Invasive Remediation (Ponytail Protocol):** Automated code fixes must be framework-idiomatic, minimal in file churn, strictly bounded, and verified via pre-flight dry-runs and automated test passes.
5. **Technical Honesty & Transparent Confidence:** Findings are scored via an auditable 0–100 mathematical rubric. If source code evidence is insufficient to prove exploitability, findings are downgraded to `Needs Review` rather than reported as false alarms.
6. **Zero-Telemetry Local Privacy:** All code scanning, evidence parsing, and report generation execute locally within the target repository workspace.

---

## 3. High-Level Architecture

The TorusGuard system architecture decomposes into four primary sub-systems:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                          AI Agent & User Interface                          │
│        (CLI Commands: /torusguard init, audit, verify, harden, apply, recheck)│
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                            Core Workflow Engine                             │
│  ┌──────────────────────┐  ┌─────────────────────┐  ┌────────────────────┐  │
│  │   Lifecycle Manager  │  │ Provenance Tracker  │  │ Confidence Scorer  │  │
│  └──────────────────────┘  └─────────────────────┘  └────────────────────┘  │
│  ┌──────────────────────┐  ┌─────────────────────┐  ┌────────────────────┐  │
│  │ Evidence Collector   │  │ Report Formatter    │  │ Masking Subsystem  │  │
│  └──────────────────────┘  └─────────────────────┘  └────────────────────┘  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                    Detection & Remediation Catalog Layer                    │
│  ┌──────────────────────┐  ┌─────────────────────┐  ┌────────────────────┐  │
│  │ 64+ Rule Modules     │  │ Framework Guides    │  │ Ponytail Patch Gen │  │
│  │ (TG-SEC, TG-AUTH...) │  │ (Django, FastAPI...)│  │ (Before/After Diff)│  │
│  └──────────────────────┘  └─────────────────────┘  └────────────────────┘  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                     Validation & Verification Harness                       │
│  ┌──────────────────────┐  ┌─────────────────────┐  ┌────────────────────┐  │
│  │ Replay Runner        │  │ Differential Comp.  │  │ Large-Project Suite│  │
│  └──────────────────────┘  └─────────────────────┘  └────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. System Context

TorusGuard operates in the local execution context of a development environment or CI container:

```text
               ┌──────────────────────────────────────────────┐
               │              Target Repository               │
               │   (Source Code, Lockfiles, Configs, Tests)   │
               └──────────────────────┬───────────────────────┘
                                      │
               ┌──────────────────────▼───────────────────────┐
               │              TorusGuard Engine               │
               │  - Reads: Rules, Schemas, Target AST/Files   │
               │  - Evaluates: Confidence Rubric, Dataflow    │
               │  - Emits: Reports, Patches, Verification Log │
               └──────────────────────┬───────────────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         ▼                            ▼                            ▼
┌──────────────────┐        ┌──────────────────┐        ┌──────────────────┐
│ Markdown Reports │        │ Isolated Runs    │        │ Hardened Patches │
│ (Audit / Triage) │        │ (.torusguard/...)│        │ (Git Diffs)      │
└──────────────────┘        └──────────────────┘        └──────────────────┘
```

---

## 5. Layered Architecture

The system is organized into five discrete horizontal layers:

1. **Interface Layer (`skills/` & CLI):** Exposes agent skill manifests (`SKILL.md`), command parsing, and workflow entrypoints.
2. **Orchestration Layer (`core/`):** Manages finding state transitions, provenance tracking, evidence hashing, and output formatting.
3. **Rules & Knowledge Layer (`rules/`, `guides/`):** Contains formal CWE/ASVS-aligned vulnerability definitions, unsafe patterns, and framework-native remediations.
4. **Schema & Contract Layer (`schemas/`):** JSON Schema definitions enforcing structured contracts for findings, evidence, confidence, provenance, and rechecks.
5. **Validation & Quality Layer (`harness/`, `tests/`):** Automated test fixtures, differential test suites, multi-repository test harnesses, and regression trackers.

---

## 6. Component Architecture

### 6.1. Lifecycle Manager (`core/models.py`)
Enforces valid state transitions across the 6-stage finding lifecycle. Ensures findings cannot be closed without verified rechecks.

### 6.2. Confidence Scorer (`core/confidence.py`)
Computes auditable 0–100 scores across 5 dimensions:
- $E_q$: Evidence Quality (0–25)
- $R_p$: Reproduction Path (0–25)
- $C_f$: Multi-signal Confirmation (0–20)
- $D_c$: Deployment Context (0–15)
- $M_r$: Manual Review Exclusions (0–15)

### 6.3. Sensitive Data Masker (`core/formatter.py`)
Automated regex-based redactor that replaces Stripe secret keys, GitHub PATs, JWTs, AWS credentials, and generic passwords with masked placeholders before writing evidence to disk.

### 6.4. Rule Catalog (`rules/`)
70+ modular security rules organized by vulnerability taxonomy:
- `TG-AUTH-*`: Authentication, Session, and RBAC security
- `TG-DB-*`: Database query isolation and credential separation
- `TG-INPUT-*`: Input sanitization, SQLi, SSTI, and path traversal
- `TG-SEC-*`: Secrets, environment variables, and log hygiene
- `TG-PLATFORM-*`: CORS, security headers, error handling
- `TG-RATE-*`: Rate limits and unbounded resource consumption
- `TG-SSRF-*`: Outbound request validation and network boundaries
- `TG-WEBHOOK-*`: Signature validation and replay mitigation
- `TG-GQL-*`: GraphQL depth, complexity, and authorization
- `TG-WS-*`: WebSocket handshakes, channel auth, and message limits
- `TG-EDGE-*`: Cloudflare Workers, Edge Isolates, and Lambda cold-start security
- `TG-AGENT-*`: Agentic AI prompt injection, MCP tool scoping, and memory leakage

### 6.5. Specialist Agent Roles (`.torusguard/agents/`)
Formal separation of responsibilities to eliminate AI confirmation bias:
- **Profiler (`profiler.md`):** Stack profiling, route discovery, framework AST inspection.
- **Auditor (`auditor.md`):** Static AST scanning, line-shift invariant fingerprinting, root-cause clustering.
- **Validator (`validator.md`):** Runtime HTTP/browser probing, token redaction, bounded exploitability checks.
- **Remediator (`remediator.md`):** Governed remediation bundles, minimal patch plans, Before/After diffs.
- **Reviewer (`reviewer.md`):** Scoped recheck verification, regression detection, SARIF v2.1.0 sign-off.

### 6.6. Two-Tier Command Engine
- **Interactive Workflows (`.torusguard/workflows/<cmd>.md`):** Structured playbooks for 11 slash commands + `/torusguard full`.
- **Specialist Skills (`.torusguard/skills/torusguard-<cmd>/SKILL.md`):** Focused, lazy-loaded domain expertise preserving context budgets.

---

## 7. Request Lifecycle

The standard audit execution follows a deterministic sequential flow:

```text
User / Agent Trigger (/torusguard audit)
   │
   ▼
1. Discovery & Stack Detection
   ├─ Detect frameworks (Django, FastAPI, Express, Next.js, etc.)
   └─ Identify exclusion patterns (.venv, node_modules, migrations)
   │
   ▼
2. Static Analysis & Pattern Match
   ├─ Evaluate active rule catalog against repository AST/source
   └─ Collect raw code evidence snippets
   │
   ▼
3. Evidence Packaging & Provenance
   ├─ Compute SHA-256 evidence checksums
   ├─ Apply sensitive data masking
   └─ Calculate 0-100 confidence scores
   │
   ▼
4. Triage & Priority Classification
   ├─ Categorize findings: Immediate (P0), Near-Term (P1), Backlog (P2)
   └─ Downgrade ambiguous findings to Needs Review
   │
   ▼
5. Artifact Generation & Storage
   ├─ Write structured Markdown report
   └─ Output run folder (.torusguard/runs/run-<timestamp>-<id>/)
```

---

## 8. Data Flow Architecture

```text
Repository Files ──► [Stack Detector] ──► Active Rule Subset
                           │
                           ▼
[Source Parser] ──► AST / Token Stream ──► [Rule Matcher]
                                                 │
                                                 ▼
[Evidence Collector] ◄── Raw Code Snippets ◄─────┘
         │
         ├──► [Masking Subsystem] ──► Redacted Snippets
         ├──► [SHA-256 Engine]   ──► Evidence Checksums
         └──► [Confidence Engine]──► Score (0-100)
                                           │
                                           ▼
                                [Finding Data Model]
                                           │
                                           ▼
                                [9-Section Formatter]
                                           │
                                           ▼
                              docs/validation/report.md
```

---

## 9. Technology Stack

- **Core Engine:** Python 3.10+ (Standard Library: `json`, `hashlib`, `re`, `pathlib`, `dataclasses`).
- **Data Contracts:** JSON Schema Draft-07 (`schemas/*.schema.json`).
- **Rule Definitions:** GitHub Flavored Markdown (GFM) with YAML Frontmatter.
- **Agent Skill Standard:** Open `skills` specification (`skills/torusguard/SKILL.md`).
- **Harness & Automation:** Pytest / Standard Python unittest harness.
- **Target Environments:** Node.js / TypeScript, Python (Django, DRF, FastAPI, Flask, SQLAlchemy).

---

## 10. Non-Functional Requirements

- **Performance:** Complete static scan of 10,000 files in $< 15$ seconds without worker thread exhaustion.
- **Memory Footprint:** Peak memory usage $< 250\text{ MB}$ during large codebase analysis.
- **Portability:** Zero binary dependencies; runs identically across Windows, macOS, and Linux.
- **Reproducibility:** Multi-pass deterministic replay guaranteeing identical findings and SHA-256 output hashes.
- **Auditability:** Every finding includes full provenance decision chains and exact source line references.

---

## 11. Cross-Cutting Concerns

- **Security & Privacy:** Local execution guarantee. Zero cloud API calls or telemetry beacons.
- **Error Handling:** Robust isolation—syntax errors in target files do not halt portfolio validation.
- **Redaction:** Automatic masking of sensitive secrets in evidence outputs.
- **Backward Compatibility:** Schema evolution adheres to strict Semantic Versioning.

---

## 12. Module Dependency Map

```text
skills/torusguard/SKILL.md
   └──► core/models.py
          ├──► schemas/finding.schema.json
          ├──► schemas/evidence.schema.json
          └──► core/confidence.py
                 └──► core/formatter.py
                        └──► templates/audit-report.template.md
```

---

## 13. Integration Points

1. **AI Agent IDE Integration:** Cursor, Antigravity IDE, Claude Code, Cline, Codex via standard slash commands.
2. **Issue Trackers:** Generates ticket-ready Markdown payloads for GitHub Issues, Jira, and Linear.
3. **CI/CD Quality Gates:** GitHub Actions / GitLab CI exit-code evaluation on blocking P0 findings.
4. **Security Information & Event Management (SIEM):** Structured JSON output emission for enterprise ingestion.

---

## 14. Scalability Strategy

- **Multi-Repository Manifests (`projects/manifest.yaml`):** Batch validation across arbitrary portfolio sizes.
- **Selective Scanning:** Framework-specific rule pruning to avoid executing irrelevant rule checks.
- **Incremental Diff Analysis:** Scans only git-modified files during `/torusguard recheck`.

---

## 15. Failure Handling & Resilience

- **Parse Failures:** Malformed source files trigger localized warnings without aborting overall repository scan.
- **Missing Context:** Unverifiable dependencies gracefully downgrade findings to `Needs Review` rather than failing.
- **Cleanup Resilience:** Robust multi-platform directory cleanup handles file locks on Windows environments.
