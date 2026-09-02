# TorusGuard Detection Engine Architecture

## 1. Overview
The TorusGuard Detection Engine is a framework-aware, context-sensitive static analysis subsystem designed to identify high-risk vulnerability patterns while strictly controlling false positive rates.

---

## 2. Detection Pipeline Architecture

The detection engine operates across four sequential evaluation stages:

```text
Source Files ──► [1. Stack Detector] ──► Active Rules Selected
                        │
                        ▼
                 [2. AST & Heuristic Matcher] ──► Raw Candidate Signals
                        │
                        ▼
                 [3. Context & Guardrail Filter] ──► Filtered / Downgraded Candidates
                        │
                        ▼
                 [4. Confidence Rubric Evaluator] ──► Verified Findings
```

### Stage 1: Stack Detection & Rule Pruning
The engine inspects workspace indicators (e.g. `manage.py`, `pyproject.toml`, `package.json`, `requirements.txt`) to determine active frameworks. Irrelevant rules are pruned before AST processing to maintain sub-second performance.

### Stage 2: AST & Heuristic Matching
Combines abstract syntax tree traversal with semantic regular expressions to detect high-risk patterns (such as unescaped rendering, unparameterized queries, raw secret string assignments, or unvalidated request headers).

### Stage 3: Context-Aware Guardrails (v0.5.6 Tuning)
To prevent systematic false positives, the engine checks for framework-native mitigation boundaries:
- **`TG-AUTH-008` (Untrusted Role Headers):** Escalates only when client-controlled headers directly assign authorization or tenant scope without server-side validation. If handled via API Gateway/mTLS, status is downgraded to `Needs Review`.
- **`TG-INPUT-005` (Template Escaping):** Differentiates autoescaped framework rendering (e.g. `render_template("foo.html", x=val)`) from explicit escaping bypasses (`| safe`, `mark_safe()`).
- **`TG-INPUT-006` (Path Traversal):** Differentiates benign `os.path.join()` from unsanitized user-supplied paths reaching disk I/O. Recognizes standard sanitizers (e.g. `secure_filename()`).
- **`TG-DB-004` (Tenant Query Isolation):** Detects tenant-scoped managers, repositories, `get_queryset()` filters, and dependency-injected tenant context before flagging primary-key lookups.
- **`TG-EDGE-001` (Edge Isolate Memory Leaks):** Differentiates read-only global constants from mutable in-memory cache dictionaries in Cloudflare Workers and Edge runtimes.
- **`TG-AGENT-001` (Prompt Injection Boundaries):** Detects user inputs concatenated into LLM system prompts without explicit XML/markdown encapsulation delimiters.
- **`TG-AGENT-002` (Unsandboxed Tool Execution):** Verifies that agent shell tool callers enforce sandbox environments, command allowlists, and execution timeouts.

### Stage 4: Mathematical Confidence Rubric
Every surviving candidate finding is evaluated against an objective 0–100 scoring model:
$$\text{Score} = E_q (0\text{--}25) + R_p (0\text{--}25) + C_f (0\text{--}20) + D_c (0\text{--}15) + M_r (0\text{--}15)$$

- **$\ge 90$ Points:** `Confirmed` (Clear evidence of exploitability in local source).
- **$70\text{--}89$ Points:** `High Confidence` (Strong static signal, framework context verified).
- **$< 70$ Points:** `Needs Review` (Ambiguous external dependencies or multi-layer abstraction).

---

## 3. Seeded-Case Recall Benchmarking
The engine incorporates a formal recall benchmarking suite (`projects/manifest.yaml`). Known non-production vulnerability seeds are injected into target repositories to ensure rule tuning does not introduce false negatives or degrade true detection capability.
