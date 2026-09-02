# TorusGuard Project Structure & Module Organization

## 1. Overview
This document outlines the directory structure, file organization standards, and functional responsibilities across the TorusGuard repository as of **v0.9.2**.

---

## 2. Directory Tree

```text
TorusGuard/
├── .torusguard/                       # Self-contained project security workspace
│   ├── TORUSGUARD.md                  # Master always-on security rules & Ponytail bounds
│   ├── ARCHITECTURE.md                # System lifecycle flowcharts & role handoff contracts
│   ├── .manifest.json                 # Cryptographic SHA-256 integrity manifest (88 files)
│   ├── config/                        # Project runtime configuration
│   │   ├── torusguard.json            # Severity thresholds, paths, governance limits
│   │   ├── slash-commands.json        # 11 slash command definitions & metadata
│   │   └── scope.json                 # Legal target authorization whitelist & TTL
│   ├── workflows/                     # 11 interactive slash command playbooks
│   │   ├── init.md, authorize.md, audit.md, verify.md, web-validate.md...
│   ├── agents/                        # 5 specialist agent definitions
│   │   ├── profiler.md, auditor.md, validator.md, remediator.md, reviewer.md
│   ├── skills/                        # Specialist skills mirror (13 skills)
│   ├── scripts/                       # Pure Python CLI automation utilities
│   │   ├── stack_detect.py            # Framework auto-detection
│   │   ├── finding_scorer.py          # 0-100 confidence scoring engine
│   │   ├── sarif_exporter.py          # OASIS SARIF v2.1.0 generator
│   │   ├── run_manager.py             # Isolated run folder lifecycle
│   │   ├── safety_gate.py             # Pre-probe safety policy evaluator
│   │   └── manifest_builder.py        # Cryptographic manifest checker & writer
│   ├── rules/                         # Active rules catalog
│   │   ├── active/                    # Dynamically activated framework rules
│   │   ├── README.md                  # Rule taxonomy & structure guide
│   │   └── TORUSGUARD.md              # Dual-path rules mirror
│   ├── references/                    # 10 self-contained framework security guides
│   │   ├── django-security.md, fastapi-security.md, nextjs-security.md...
│   ├── templates/                     # Standard markdown output templates
│   └── runs/                          # Isolated execution history folders
│
├── skills/                            # Decoupled AI Agent Skill Packages
│   ├── torusguard/                    # Root router & workspace bootstrapper
│   │   ├── SKILL.md                   # Compact router (58 lines)
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
│   └── torusguard-full/               # Master 7-stage orchestrator skill
│
├── rules/                             # 70+ documented security rules (Markdown + Frontmatter)
│   ├── agent/                         # TG-AGENT-* AI agent & prompt injection rules
│   ├── edge/                          # TG-EDGE-* Cloudflare Workers & Lambda rules
│   ├── authorization/                 # TG-AUTH-* rules
│   ├── business-logic/                # TG-BIZ-* rules
│   ├── cache/                         # TG-CACHE-* rules
│   ├── csrf/                          # TG-CSRF-* rules
│   ├── graphql/                       # TG-GQL-* rules
│   ├── secrets/                       # TG-SEC-* rules
│   ├── ssrf/                          # TG-SSRF-* rules
│   ├── supply-chain/                  # TG-SUPPLY-* rules
│   ├── webhook/                       # TG-WEBHOOK-* rules
│   └── websocket/                     # TG-WS-* rules
│
├── schemas/                           # JSON Schema Draft-07 formal data contracts
│   ├── finding.schema.json            # Canonical finding object schema
│   ├── evidence.schema.json           # Evidence packaging and SHA-256 typing
│   ├── remediation.schema.json        # Ponytail patch and diff specification
│   ├── rule.schema.json               # Rule metadata, CWE, ASVS mapping schema
│   ├── lifecycle.schema.json          # 7-stage finding lifecycle transition schema
│   ├── provenance.schema.json         # Provenance chain and decision path schema
│   ├── confidence.schema.json         # 0-100 mathematical confidence rubric schema
│   ├── retest.schema.json             # Post-fix verification and recheck schema
│   ├── authorization.schema.json      # Legal target authorization schema
│   ├── runtime-evidence.schema.json   # Runtime HTTP/browser evidence schema
│   └── replay-trace.schema.json       # Deterministic replay trace schema
│
├── harness/                           # 9 Automated Test Suites (381 Test Assertions)
│   ├── runner.py                      # Core schemas & confidence harness (75 tests)
│   ├── validate_v0_9_2_workflows_and_skills.py # Workflows & skills engine suite (35 tests)
│   ├── validate_v0_9_1_installer.py   # Simulation installer suite (14 tests)
│   ├── validate_v0_9_0_skills.py      # Granular skills suite (53 tests)
│   ├── validate_v0_7_0_runtime.py     # Senior QA runtime suite (67 tests)
│   ├── validate_v0_8_0_part1.py       # Workspace foundation suite (11 tests)
│   ├── validate_v0_8_0_part2.py       # Agents & workflows suite (20 tests)
│   ├── validate_v0_8_0_part3.py       # Scripts & references suite (18 tests)
│   └── engine/                        # Validation engine subsystem
│
├── install.py                         # Standalone zero-dependency CLI installer
├── guides/                            # In-depth framework implementation guides
├── examples/                          # Paired vulnerable vs hardened educational apps
├── docs/                              # Comprehensive documentation suite
│   ├── architecture/                  # System architecture specifications
│   ├── releases/                      # Release notes (v0.1.0 through v0.9.2)
│   ├── workflow/                      # Lifecycle and triage guides
│   ├── overview/                      # Security philosophy and core principles
│   └── validation/                    # Validation reports & portfolio summaries
│
└── tests/                             # Regression test fixtures & layout fixtures
```

---

## 3. File Naming & Code Style Standards
- **Rule Definitions:** `TG-<CATEGORY>-<NUMBER>-<slug>.md` (e.g. `TG-AGENT-001-prompt-injection-system-context.md`).
- **Workflows:** `<command-name>.md` in `.torusguard/workflows/`.
- **Specialist Skills:** `torusguard-<command-name>/SKILL.md` in `skills/` and `.torusguard/skills/`.
- **Schemas:** `<entity>.schema.json` (lowercase with hyphenated slugs).
- **Release Notes:** `v<major>.<minor>.<patch>.md` in `docs/releases/`.
- **Validation Reports:** `<target>-v<version>-validation.md` in `docs/validation/`.
