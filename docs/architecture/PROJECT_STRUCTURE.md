# TorusGuard Project Structure & Module Organization

## 1. Overview
This document outlines the directory structure, file organization standards, and functional responsibilities across the TorusGuard repository.

---

## 2. Directory Tree

```text
TorusGuard/
├── schemas/                       # JSON Schema Draft-07 formal data contracts
│   ├── finding.schema.json        # Canonical finding object schema
│   ├── evidence.schema.json       # Evidence packaging and SHA-256 typing
│   ├── remediation.schema.json    # Ponytail patch and diff specification
│   ├── rule.schema.json           # Rule metadata, CWE, ASVS mapping schema
│   ├── lifecycle.schema.json      # 6-stage finding lifecycle transition schema
│   ├── provenance.schema.json     # Provenance chain and decision path schema
│   ├── confidence.schema.json     # 0-100 mathematical confidence rubric schema
│   ├── retest.schema.json         # Post-fix verification and recheck schema
│   ├── fixture.schema.json        # Test fixture specification schema
│   └── validation-run.schema.json # Multi-project portfolio run schema
│
├── core/                          # Python core engine models & formatting logic
│   ├── models.py                  # Dataclasses and finding state machine
│   ├── confidence.py              # 5-factor confidence scoring calculator
│   ├── provenance.py              # Provenance tracker and evidence hasher
│   └── formatter.py               # Human-First 9-section report formatter
│
├── harness/                       # Test runners and validation engines
│   ├── runner.py                  # Core validation suite runner (66 tests)
│   ├── validate_large_projects.py # Multi-repository large-project validation runner
│   └── engine/                    # 7-layer validation engine subsystem
│       ├── fixture_manager.py     # Educational & regression fixture manager
│       ├── replay_runner.py       # Deterministic 3-pass replay executor
│       ├── result_comparator.py   # Vulnerable vs hardened diff comparator
│       ├── regression_tracker.py  # Historical regression tracker
│       ├── false_positive_analyzer.py # False-alarm root cause analyzer
│       ├── evidence_collector.py  # Environment snapshot and evidence collector
│       └── report_emitter.py      # Markdown validation report emitter
│
├── projects/                      # Validation benchmarks and manifests
│   └── manifest.yaml              # 10 large-project repository definitions & seeds
│
├── skills/                        # AI Agent Skill manifests
│   └── torusguard/
│       ├── SKILL.md               # Main portable skill definition with YAML frontmatter
│       └── references/            # 23 stack-specific reference cheat-sheets
│
├── rules/                         # 64+ documented security rules (Markdown + Frontmatter)
│   ├── authorization/             # TG-AUTH-* rules
│   ├── business-logic/            # TG-BIZ-* rules
│   ├── cache/                     # TG-CACHE-* rules
│   ├── csrf/                      # TG-CSRF-* rules
│   ├── graphql/                   # TG-GQL-* rules
│   ├── secrets/                   # TG-SEC-* rules
│   ├── ssrf/                      # TG-SSRF-* rules
│   ├── supply-chain/              # TG-SUPPLY-* rules
│   ├── webhook/                   # TG-WEBHOOK-* rules
│   └── websocket/                 # TG-WS-* rules
│
├── templates/                     # Reusable security document templates
│   ├── SECURITY.template.md       # Standard project security policy
│   ├── audit-report.template.md   # 9-section human-first audit report
│   ├── threat-model.template.md   # Application threat model template
│   └── deployment-preflight.template.md # Pre-flight release checklist
│
├── guides/                        # In-depth framework implementation guides
│   ├── python/                    # Django, DRF, FastAPI, Flask, SQLAlchemy
│   └── javascript/                # React, Next.js, Express, Supabase, Firebase
│
├── examples/                      # Paired vulnerable vs hardened educational apps
│   ├── python/                    # Python framework reference applications
│   └── react-express/             # JavaScript full-stack reference applications
│
├── docs/                          # Architectural documentation and release notes
│   ├── architecture/              # 10 formal system architecture specifications
│   ├── releases/                  # Release notes (v0.2.0 through v0.5.6)
│   ├── workflow/                  # Lifecycle and triage guides
│   └── validation/                # Validation reports & portfolio summaries
│
└── tests/                         # Regression test fixtures & layout fixtures
    └── fixtures/                  # Stack detection and differential test cases
```

---

## 3. File Naming & Code Style Standards
- **Rule Definitions:** `TG-<CATEGORY>-<NUMBER>-<slug>.md` (e.g. `TG-AUTH-008-untrusted-role-header-injection.md`).
- **Schemas:** `<entity>.schema.json` (lowercase with hyphenated slugs).
- **Release Notes:** `v<major>.<minor>.<patch>.md` in `docs/releases/`.
- **Validation Reports:** `<target>-v<version>-validation.md` in `docs/validation/`.
