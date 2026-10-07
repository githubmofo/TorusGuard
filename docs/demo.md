# 🚀 TorusGuard Quickstart & Demo Guide (v2.2.0)

> Experience TorusGuard's full security lifecycle in under 2 minutes.  
> Works identically via **npx** (Node.js), the standalone **Go binary**, or **AI Chat Slash Commands**.

---

## ⚡ 60-Second Quick Demo

### Step 1: Run the Interactive Command Center (Zero Arguments)

The fastest way to experience TorusGuard without memorizing any flags:

```bash
# Option A: via npx (zero installation)
npx torusguard

# Option B: via Go binary
./torusguard.exe
# on Linux/macOS: ./torusguard
```

**Interactive Terminal Dashboard:**
```text
  ╭───────────────────────────────────────────────────────────────────────╮
  │                                                                       │
  │  🛡️  TORUSGUARD COMMAND CENTER                                v2.2.0  │
  │  Interactive Security Engine                                          │
  │                                                                       │
  ╰───────────────────────────────────────────────────────────────────────╯
  ┌─ Quick Actions ───────────────────────────────────────────────────────┐
  │  [1]   🚀 Audit Workspace          (Full AST & Taint Scan)            │
  │  [2]   👁️  OCR Vision Scan          (Images & Diagram Secrets)         │
  │  [3]   📊 Posture Status           (Active Posture & Rules)           │
  │  [4]   🐳 Container Audit          (Dockerfile & Compose Scan)        │
  │  [5]   ⚡ ReDoS Complexity Scan    (Catastrophic Regex Scan)          │
  │  [6]   🤖 AI & RAG Defense         (Prompt Injection & Vectors)       │
  │  [7]   🔍 Git History Mine         (Committed Leaks & Tokens)         │
  │  [8]   🛡️  Harden Candidates       (Ponytail Bounded Patches)         │
  │  [9]   📑 Posture Report           (Generate Visual HTML Report)      │
  │  [10]  📖 Awesome Rules Catalog    (88 Rules Across 22 Families)      │
  │  [0]   ❌ Exit                                                        │
  └───────────────────────────────────────────────────────────────────────┘
```
Simply enter a number (e.g. `1` or `2`) to execute that command!

---

## 🔍 Step-by-Step Command Demo

### Step 1: Initialize Workspace (`init`)

Scaffold the `.torusguard/` workspace and activate 88 security rules across 22 architectural families:

```bash
npx torusguard init
# or: ./torusguard.exe init
```

**Output:**
```text
┌─ TORUSGUARD INITIALIZATION ─────────────────────────────────────────┐
│ Status: Workspace successfully initialized                          │
│ Stack: Node.js (TypeScript), Go 1.25                                │
│ Rules: 88 security invariants activated across 22 families          │
│ Ledger: Synchronized living security_report.md                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

### Step 2: Scan Visual Assets for Leaked Secrets (`ocr-scan`)

Inspect diagrams, cloud architecture maps, and screenshots with the **Hybrid First-Principles Vision OCR engine** (zero external dependencies required):

```bash
# Auto-discover and scan all images in the project:
npx torusguard ocr-scan

# Or scan a specific file or folder:
npx torusguard ocr-scan docs/architecture.png
```

**Output:**
```text
┌─ OCR VISION SECRET SCAN ─────────────────────────────────────────────┐
│ Target: docs/architecture.png                                        │
│ Engine: Hybrid First-Principles + Tesseract OCR                      │
│ Status: 1 Leaked Credential Detected                                 │
│                                                                      │
│ ✖ TG-SEC-002: AWS Access Key ID Detected                             │
│   Extracted: AKIA**************** (Redacted for safety)              │
│   Remediation: Invalidate key in AWS IAM and move to Vault / Env     │
└──────────────────────────────────────────────────────────────────────┘
```

---

### Step 3: Run Full AST & Taint Audit (`audit`)

Perform deep polyglot AST traversal, interprocedural taint flow tracking, and first-principles checks:

```bash
npx torusguard audit
# or: ./torusguard.exe audit
```

**Output:**
```text
┌─ SECURITY AUDIT COMPLETE ───────────────────────────────────────────┐
│ Scanned: 42 files across 4 languages (Go, TS, Python, Docker)        │
│ Findings: 3 Open (1 Critical, 1 High, 1 Medium)                      │
│ Confidence: 7-Signal Calibrated (92% Average)                        │
│ Ledger: Synchronized security_report.md                             │
└─────────────────────────────────────────────────────────────────────┘
```

---

### Step 4: Formulate & Apply Surgical Patches (`harden` & `apply`)

Validate candidate patches against Ponytail Protocol bounds ($\le 35$ additions, $\le 25$ deletions) and apply them with automatic `.bak` snapshots:

```bash
# 1. Validate patch bounds
npx torusguard harden candidate.patch

# 2. Apply patch with Human Gate authorization
npx torusguard apply --yes candidate.patch

# 3. Differential recheck confirming zero regressions
npx torusguard recheck

# 4. Instant rollback if needed
npx torusguard rollback
```

---

### Step 5: Export Posture Reports (`report`)

Generate single-file visual dark-mode HTML dashboards or OASIS SARIF v2.1.0 logs:

```bash
# Generate visual dark-mode HTML dashboard
npx torusguard report --html

# Export OASIS SARIF v2.1.0 for GitHub Advanced Security
npx torusguard report --sarif
```

---

## 🤖 AI Chat Slash Command Demo

In any supported AI coding assistant (Cursor, Claude Code, Windsurf, Antigravity, Copilot):

```text
/torusguard init          → Profiles workspace and activates TG-* rules
/torusguard ocr-scan      → Scans diagrams & screenshots for leaked keys
/torusguard audit         → Runs AST security audit and updates security_report.md
/torusguard harden        → Validates candidate patches against Ponytail bounds
/torusguard apply         → Prompts Human Gate and applies with .bak backup
/torusguard recheck       → Verifies fix closure with zero regressions
/torusguard report        → Emits visual HTML dashboard
```

TorusGuard guarantees 100% tri-mode parity between your terminal, your AI chat assistant, and native MCP agent tool calls.
