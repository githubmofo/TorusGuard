# TorusGuard Detection Engine Architecture

## 1. Overview
The TorusGuard Detection Engine is a framework-aware, context-sensitive static analysis subsystem designed to identify high-risk vulnerability patterns while strictly controlling false positive rates across any programming language, framework, or library.

---

## 2. Detection Pipeline Architecture

The detection engine operates across five sequential evaluation stages:

```text
Source Files ──► [1. Universal Polyglot Profiler] ──► Language & Frameworks Selected
                         │
                         ▼
                  [2. AST & Heuristic Matcher] ──► Raw Candidate Signals
                         │
                         ▼
                  [3. Context & Guardrail Filter] ──► Filtered / Downgraded Candidates
                         │
                         ▼
                  [4. Confidence Rubric Evaluator] ──► Verified Findings (0–100)
                         │
                         ▼
                  [5. Polyglot Diff Guard] ──► Pre-Merge Regression Interception
```

### Stage 1: Universal Polyglot Profiling (`stack_detect.py` & `core/stack_profiler.py`)
The engine inspects workspace manifest indicators and dependency catalogs across 16+ programming languages:
- **Go:** `go.mod` (detects Gin, Fiber, Echo, Chi, GORM, Ent, SQLx).
- **Rust:** `Cargo.toml` (detects Actix-web, Axum, Rocket, Diesel, SeaORM, SQLx).
- **Java:** `pom.xml`, `build.gradle` (detects Spring Boot, Quarkus, Micronaut, Hibernate, JPA, MyBatis, jOOQ).
- **C# (.NET):** `*.csproj`, `*.sln` (detects ASP.NET Core, Blazor, Entity Framework Core, Dapper).
- **PHP:** `composer.json` (detects Laravel, Symfony, Slim, Eloquent, Doctrine).
- **Ruby:** `Gemfile` (detects Ruby on Rails, Sinatra, ActiveRecord, Sequel).
- **Kotlin:** `build.gradle.kts` (detects Spring Boot, Ktor, Exposed).
- **Elixir:** `mix.exs` (detects Phoenix, Ecto).
- **Dart:** `pubspec.yaml` (detects Flutter, Shelf, Drift).
- **C / C++:** `CMakeLists.txt`, `Makefile` (detects Crow, Drogon, Oat++).
- **Python:** `pyproject.toml`, `requirements.txt`, `manage.py` (detects FastAPI, Django, Flask, DRF, SQLAlchemy).
- **TypeScript / JavaScript:** `package.json` (detects Next.js, Express, NestJS, Vite, Nuxt, Prisma, Drizzle, TypeORM).

#### Fallback Extension Census
If manifest files are absent or located in non-standard subdirectories, the engine performs a recursive source extension census (`.go`, `.rs`, `.java`, `.cs`, `.php`, `.rb`, `.kt`, `.ex`, `.dart`, `.cpp`, `.py`, `.ts`, `.js`) to select the dominant runtime environment automatically.

#### Monorepo Fleet Discovery (`scripts/monorepo_detector.py`)
In complex workspaces, the engine maps monorepo architectures (pnpm/npm/yarn workspaces, Cargo workspaces, Go multi-module workspaces, Gradle multi-project builds). Each sub-package is profiled independently, ensuring package-level framework and ORM rules apply accurately without cross-package interference.

### Stage 2: AST & Heuristic Matching
Combines abstract syntax tree traversal with semantic regular expressions to detect high-risk patterns (such as unescaped rendering, unparameterized queries, raw secret string assignments, or unvalidated request headers).

### Stage 3: Context-Aware Guardrails
To prevent systematic false positives, the engine checks for framework-native mitigation boundaries and operational context:
- **Context-Aware Test-Path False Positive Suppression (`is_test_path()`):** Test suites, mocks, and fixtures located in `test/`, `tests/`, `spec/`, `__tests__/`, or test harness files often contain intentional dummy credentials, bypasses, or mock tokens. The engine automatically discounts non-production test harnesses to eliminate false alarms.
- **`TG-AUTH-008` (Untrusted Role Headers):** Escalates only when client-controlled headers directly assign authorization or tenant scope without server-side validation. If handled via API Gateway/mTLS, status is downgraded to `Needs Review`.
- **`TG-INPUT-005` (Template Escaping):** Differentiates autoescaped framework rendering (e.g. `render_template("foo.html", x=val)`) from explicit escaping bypasses (`| safe`, `mark_safe()`).
- **`TG-INPUT-006` (Path Traversal):** Differentiates benign `os.path.join()` from unsanitized user-supplied paths reaching disk I/O. Recognizes standard sanitizers (e.g. `secure_filename()`).
- **`TG-DB-004` (Tenant Query Isolation):** Detects tenant-scoped managers, repositories, `get_queryset()` filters, and dependency-injected tenant context before flagging primary-key lookups.
- **`TG-EDGE-001` (Edge Isolate Memory Leaks):** Differentiates read-only global constants from mutable in-memory cache dictionaries in Cloudflare Workers and Edge runtimes.
- **`TG-AGENT-001` (Prompt Injection Boundaries):** Detects user inputs concatenated into LLM system prompts without explicit XML/markdown encapsulation delimiters.
- **`TG-AGENT-002` (Unsandboxed Tool Execution):** Verifies that agent shell tool callers enforce sandbox environments, command allowlists, and execution timeouts.

### Stage 4: Mathematical Confidence Rubric
Every surviving candidate finding is evaluated against an objective 0–100 scoring model:
$$\text{Score} = (w_d \cdot D) + (w_e \cdot E) + (w_c \cdot C_{ast}) + \text{MemoryBoost} - P_{fp} - P_{drift}$$

- **$\ge 90$ Points:** `Confirmed` (Clear evidence of exploitability in local source).
- **$70\text{--}89$ Points:** `High Confidence` (Strong static signal, framework context verified).
- **$< 70$ Points:** `Needs Review` (Ambiguous external dependencies or multi-layer abstraction).

### Stage 5: Polyglot Content-Aware Diff Guard (`diff_guard.py`)
Intercepts risky modifications in unified diffs before code is merged:
- **Multi-Language Bypass Patterns (`TG-DIFF-001`):**
  - Go: `InsecureSkipVerify: true`, `tls.Config{InsecureSkipVerify: true}`
  - Java: `csrf().disable()`, `permitAll()`
  - C#: `[AllowAnonymous]`, `ServerCertificateCustomValidationCallback = .*true`
  - PHP: `CURLOPT_SSL_VERIFYPEER => false`, `verify => false`
  - Rust: `unsafe {`
- **Multi-ORM Tenant Boundary Stripping (`TG-DIFF-003`):**
  - GORM: Removal of `.Where("tenant_id = ?")`
  - LINQ / Entity Framework: Removal of `.Where(x => x.TenantId == ...)`
  - Prisma: Removal of `where: { tenantId: ... }`
- **Credential Ingestion (`TG-DIFF-002`):**
  - Raw JWTs, Bearer tokens, or API keys in added lines.
- **Regression Watch (`TG-DIFF-004`):**
  - Modifications re-introducing known historical vulnerabilities from `.torusguard/memory/`.
- **Pre-Commit Enforcement (`diff_guard.py --install-hook`):**
  - Installs a native `.git/hooks/pre-commit` script to block commits that violate `TG-DIFF-001` through `TG-DIFF-004` locally before pushing to upstream remotes.

### Stage 6: Living Security Report Synchronization (`report_sync.py`)
Synchronizes all AST discoveries, candidate patches, and recheck closures into `security_report.md` at workspace root:
- Single source of truth guaranteeing zero hallucination across CLI tools and AI agent chat sessions.
- Dynamic calculation of repository Health Score (0–100).
- State transitions adhere strictly to the finding lifecycle: `OPEN 🔴` $\rightarrow$ `VERIFIED 🟠` $\rightarrow$ `CANDIDATE 🟡` $\rightarrow$ `APPLIED 🔵` $\rightarrow$ `RESOLVED 🟢`.

---

## 3. High-Precision Scanner Refinements & Noise Suppression
- **Active Network Sinks (`TG-SSRF-002`):** Constrains regex scanning strictly to active HTTP network dispatch functions (`fetch`, `axios`, `requests.get`) rather than flagging benign configuration references or request URL variables (`req.url`, `config.url`).
- **Catastrophic Backtracking Mitigation (`TG-SSRF-004`):** Optimizes lookahead assertions against AWS metadata IPs (`169.254.169.254`) and cloud endpoints to prevent regex engine stalls.
- **Whole-File AST Analysis (`TG-PLATFORM-002`):** Evaluates server source files globally for the mounting of security header middleware (`helmet()`, `secure-headers`), eliminating false positive findings on individual sub-route definitions.
- **Documentation & Mock Exemptions:** Scans automatically discount markdown files (-25 pts in `finding_scorer.py`), test payloads in `tests/fixtures/payload/`, and internal framework tooling in `.torusguard/scripts/`.

---

## 4. Seeded-Case Recall Benchmarking
The engine incorporates a formal recall benchmarking suite (`projects/manifest.yaml`). Known non-production vulnerability seeds are injected into target repositories to ensure rule tuning does not introduce false negatives or degrade true detection capability.
