# TorusGuard Project Structure & Module Organization

## 1. Overview
This document outlines the directory structure, file organization standards, and functional responsibilities across the TorusGuard repository as of **v1.3.5**.

---

## 2. Directory Tree

```text
TorusGuard/
├── security_report.md                 # Root Living Security Report ground-truth ledger
├── package.json                       # NPM CLI package manifest (v1.3.5)
├── README.md                          # Master documentation & visual branding
├── AGENTS.md                          # Master security guardrails & AI agent invariants
├── SECURITY.md                        # Security policy, supported versions, and disclosures
├── CHANGELOG.md                       # Historical release log
│
├── bin/                               # Command-line entrypoints
│   └── torusguard.js                  # 14-command CLI dispatcher with 75-col terminal UI
│
├── .torusguard/                       # Self-contained project security workspace
│   ├── TORUSGUARD.md                  # Master always-on security rules & Ponytail bounds
│   ├── ARCHITECTURE.md                # System lifecycle flowcharts & role handoff contracts
│   ├── .manifest.json                 # Cryptographic SHA-256 integrity manifest
│   ├── config/                        # Project runtime configuration
│   │   ├── torusguard.json            # Severity thresholds, paths, governance limits
│   │   ├── slash-commands.json        # 14 slash command definitions & metadata
│   │   └── scope.json                 # Legal target authorization whitelist & TTL
│   ├── workflows/                     # 12 interactive slash command playbooks
│   │   ├── init.md, authorize.md, audit.md, verify.md, web-validate.md...
│   ├── agents/                        # 5 specialist agent definitions
│   │   ├── profiler.md, auditor.md, validator.md, remediator.md, reviewer.md
│   ├── skills/                        # Specialist skills mirror (13 skills)
│   ├── memory/                        # Adaptive Security Memory Engine
│   │   ├── events/                    # Append-only security event ledger
│   │   ├── patterns.json              # Distilled patterns & Golden Fix Recipes
│   │   ├── context.json               # Structured context card for AI prompts
│   │   └── profile.json               # Project security DNA & fix velocity
│   ├── scripts/                       # Pure Python CLI automation utilities
│   │   ├── audit_runner.py            # 74-rule AST static security scanner
│   │   ├── harden_runner.py           # Ponytail patch synthesizer (19 templates)
│   │   ├── apply_runner.py            # Human Gate patch applier & rollback
│   │   ├── recheck_runner.py          # Differential AST fix closure verifier
│   │   ├── report_sync.py             # Living security report ground truth engine
│   │   ├── term_ui.py                 # Standardized 75-column terminal visual engine
│   │   ├── html_reporter.py           # Standalone dark-mode visual HTML dashboard
│   │   ├── rules_sync.py              # AI IDE rules auto-sync compiler
│   │   ├── diff_guard.py              # Content-aware diff guard & pre-commit hook
│   │   ├── monorepo_detector.py       # Monorepo fleet detector across ecosystems
│   │   ├── stack_detect.py            # Universal polyglot stack profiler
│   │   ├── finding_scorer.py          # 0-100 confidence scoring engine
│   │   ├── sarif_exporter.py          # OASIS SARIF v2.1.0 generator
│   │   ├── run_manager.py             # Isolated run folder lifecycle & redactor
│   │   ├── safety_gate.py             # Pre-probe safety policy evaluator
│   │   └── manifest_builder.py        # Cryptographic manifest checker & writer
│   ├── rules/                         # Active rules catalog
│   ├── snapshots/                     # Pre-apply rollback backups (<run_id>/)
│   └── runs/                          # Isolated execution history folders
│
├── .agent/                            # Antigravity & Agentic IDE Integration
│   ├── rules/                         # GEMINI.md master rules & guardrails
│   ├── skills/                        # Modernized dual-mode specialist skills
│   └── workflows/                     # Modernized security workflows
│
├── skills/                            # Decoupled AI Agent Skill Packages
│   ├── torusguard/                    # Root router & workspace bootstrapper
│   │   ├── SKILL.md                   # Compact router
│   │   ├── bootstrap.py               # Autonomous offline workspace unpacker
│   │   └── payload/                   # Bundled offline .torusguard template
│   ├── torusguard-init/               # Stack detection & rule activation skill
│   ├── torusguard-authorize/          # Scope boundary & safety gate skill
│   ├── torusguard-audit/              # Static AST analysis & clustering skill
│   ├── torusguard-verify/             # Evidence sufficiency & scoring skill
│   ├── torusguard-web-validate/       # Authorized HTTP probing skill
│   ├── torusguard-exploit-check/      # Bounded exploitability confirmation skill
│   ├── torusguard-harden/             # Ponytail patch formulation skill
│   ├── torusguard-apply/              # Surgical patch apply & rollback skill
│   ├── torusguard-recheck/            # Targeted differential re-scan skill
│   ├── torusguard-report/             # Executive reporting & SARIF skill
│   ├── torusguard-status/             # Read-only posture inspection skill
│   ├── torusguard-recipes/            # Golden Fix Recipe exploration skill
│   └── torusguard-full/               # Master 7-stage orchestrator skill
│
├── rules/                             # 74 Documented Security Rules across 18 Families
│   ├── secrets/                       # TG-SEC-* (7 rules)
│   ├── authentication/                # TG-AUTH-* (8 rules)
│   ├── database/                      # TG-DB-* (4 rules)
│   ├── input/                         # TG-INPUT-* (6 rules)
│   ├── rate-limiting/                 # TG-RATE-* (3 rules)
│   ├── agent/                         # TG-AGENT-* (4 rules)
│   ├── ssrf/                          # TG-SSRF-* (4 rules)
│   ├── webhook/                       # TG-WEBHOOK-* (4 rules)
│   ├── websocket/                     # TG-WS-* (4 rules)
│   ├── csrf/                          # TG-CSRF-* (2 rules)
│   ├── graphql/                       # TG-GQL-* (4 rules)
│   ├── supply-chain/                  # TG-SUPPLY-* (6 rules)
│   ├── business-logic/                # TG-BIZ-* (4 rules)
│   ├── cache/                         # TG-CACHE-* (3 rules)
│   ├── client/                        # TG-CLIENT-* (2 rules)
│   ├── platform/                      # TG-PLATFORM-* (4 rules)
│   ├── diff/                          # TG-DIFF-* (3 rules)
│   └── edge/                          # TG-EDGE-* (2 rules)
│
├── schemas/                           # JSON Schema formal data contracts
│   ├── finding.schema.json            # Canonical finding object schema
│   ├── golden-recipe.schema.json      # Golden Fix Recipe schema
│   ├── evidence.schema.json           # Evidence packaging and SHA-256 typing
│   ├── remediation.schema.json        # Ponytail patch and diff specification
│   ├── rule.schema.json               # Rule metadata, CWE, ASVS mapping schema
│   ├── lifecycle.schema.json          # Finding lifecycle transition schema
│   ├── provenance.schema.json         # Provenance chain and decision path schema
│   ├── confidence.schema.json         # 0-100 mathematical confidence rubric schema
│   ├── retest.schema.json             # Post-fix verification and recheck schema
│   └── authorization.schema.json      # Legal target authorization schema
│
├── harness/                           # Automated Test Harness (81 Test Suites)
│   ├── runner.py                      # Master test runner (npm test)
│   ├── validate_v0_9_2_diff_and_monorepo.py
│   ├── validate_v1_3_0_polyglot.py
│   ├── validate_v1_2_0_rules_and_html.py
│   ├── validate_v1_1_0_advanced_memory.py
│   ├── validate_v1_0_0_memory.py
│   └── engine/                        # Validation engine subsystem
│
├── docs/                              # Comprehensive documentation suite
│   ├── architecture/                  # System architecture specifications
│   ├── releases/                      # Release notes (v0.2.0 through v1.3.5)
│   ├── workflow/                      # Lifecycle, triage, and replay guides
│   ├── overview/                      # Security philosophy and core principles
│   └── validation/                    # Multi-repo validation reports
│
└── tests/                             # Regression test fixtures & layout fixtures
```

---

## 3. File Naming & Code Style Standards
- **Rule Definitions:** `TG-<CATEGORY>-<NUMBER>-<slug>.md` (e.g. `TG-AGENT-001-prompt-injection-system-context.md`).
- **Workflows:** `<command-name>.md` in `.torusguard/workflows/` and `.agent/workflows/`.
- **Specialist Skills:** `torusguard-<command-name>/SKILL.md` in `skills/`, `.torusguard/skills/`, and `.agent/skills/`.
- **Schemas:** `<entity>.schema.json` (lowercase with hyphenated slugs).
- **Release Notes:** `v<major>.<minor>.<patch>.md` in `docs/releases/`.
- **Validation Reports:** `<target>-v<version>-validation.md` in `docs/validation/`.
