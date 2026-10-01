# 🛠️ Option 2: Build from Source Guide (Contributors & Advanced Devs)

> This guide explains how to clone, compile, and run **TorusGuard** directly from source code using the Go toolchain.  
> Recommended for contributors, security researchers, and developers extending TorusGuard with custom rules or MCP tools.

---

## 📋 Prerequisites

Before building TorusGuard from source, verify you have the following installed:

1. **Go Compiler (1.25 or later):**
   ```bash
   go version
   # Expected: go version go1.25... or higher
   ```
2. **Git:**
   ```bash
   git version
   ```
3. **Python 3.10+ (Optional):** Required only if executing the Python harness validation suites (`harness/runner.py`).

---

## 🚀 Step 1: Clone the Repository

Clone the official TorusGuard repository:

```bash
git clone https://github.com/githubmofo/TorusGuard.git
cd TorusGuard
```

---

## 🔨 Step 2: Build the Standalone Binary

TorusGuard's primary enforcement kernel is written in pure Go with zero external CGO runtime dependencies.

### On Linux / macOS:
```bash
go build -o torusguard ./cmd/torusguard
```

### On Windows (PowerShell / Command Prompt):
```powershell
go build -o torusguard.exe ./cmd/torusguard
```

---

## 🧪 Step 3: Verify the Build

Confirm that the binary compiled successfully and outputs version **v2.1.3**:

### Linux / macOS:
```bash
./torusguard --version
# Output: torusguard v2.1.3 (pure go binary)
```

### Windows:
```powershell
.\torusguard.exe --version
# Output: torusguard v2.1.3 (pure go binary)
```

---

## 💻 Step 4: Running Commands

You can run any TorusGuard lifecycle command directly using your newly built binary:

```bash
# Initialize a workspace in the current directory
./torusguard init

# Run an AST security audit against the workspace
./torusguard audit

# Inspect workspace diagnostic posture
./torusguard status

# Run SecurityReviewBench self-evaluating benchmark
./torusguard benchmark

# Synthesize STRIDE threat model & Mermaid DFDs
./torusguard threatmodel

# Run differential PR review on staged git changes
./torusguard review

# Launch native Model Context Protocol server (stdio JSON-RPC 2.0)
./torusguard mcp
```

### Analyzing another directory:
Use the `--target` or `-t` flag:

```bash
./torusguard audit --target /path/to/other/project
```

---

## 🧪 Step 5: Running Tests & Verifications

TorusGuard includes unit tests, integration suites, and performance benchmarks:

### 1. Run all Go package tests:
```bash
go test -v ./...
```

### 2. Run the SecurityReviewBench suite:
```bash
go run ./cmd/torusguard benchmark
```

### 3. Run the comprehensive multi-version Python evaluation harness:
```bash
python harness/runner.py
```

---

## 📦 Step 6: Installing to System PATH

If you want your locally compiled binary accessible everywhere across your terminal:

```bash
go install ./cmd/torusguard
```

This compiles and moves the `torusguard` binary into your `$GOPATH/bin` (or `%USERPROFILE%\go\bin` on Windows). Ensure this directory is present in your system `PATH`.

---

## 📚 Related Documentation
- [Option 1: npm & npx Usage Guide](option-1-npm.md)
- [Option 3: Go Install Guide](option-3-go-install.md)
- [Contributing Guidelines](../../CONTRIBUTING.md)
- [System Architecture](../../README.md#-autonomous-architecture--workflow)
