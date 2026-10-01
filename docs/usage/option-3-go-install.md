# 🐹 Option 3: Go Install Guide (Go Ecosystem & Standalone Binary)

> If you work in the Go ecosystem or want a single statically-compiled binary with **zero Node.js or npm dependencies**, you can install TorusGuard via `go install`.

---

## 📋 Prerequisites

- **Go 1.25+** installed on your system.
  ```bash
  go version
  # Expected: go version go1.25... or higher
  ```
- **Ensure `$GOPATH/bin` is in your `PATH`:**
  - **Linux / macOS:**
    ```bash
    export PATH="$PATH:$(go env GOPATH)/bin"
    ```
    *(Add the line above to your `~/.bashrc` or `~/.zshrc` to make it permanent).*
  - **Windows (PowerShell):**
    ```powershell
    $env:PATH += ";$((go env GOPATH))\bin"
    ```
    *(Or add `%USERPROFILE%\go\bin` to your User Environment Variables via Windows Settings).*

---

## 🚀 Step 1: Install via `go install`

Run the following command from any terminal:

```bash
go install github.com/githubmofo/TorusGuard/cmd/torusguard@latest
```

Go will fetch the repository, compile the standalone executable binary, and install it into your `$(go env GOPATH)/bin` directory.

---

## 🧪 Step 2: Verify Installation

Check that `torusguard` is reachable in your path:

### Linux / macOS:
```bash
which torusguard
torusguard --version
# Expected: torusguard v2.1.3 (pure go binary)
```

### Windows (PowerShell):
```powershell
Get-Command torusguard
torusguard --version
# Expected: torusguard v2.1.3 (pure go binary)
```

---

## 💻 Step 3: Usage Across Any Project

You can now use `torusguard` across any software project on your computer:

```bash
# Navigate to your application
cd /path/to/my-web-app

# 1. Initialize TorusGuard governance workspace
torusguard init

# 2. Run static AST security scan
torusguard audit

# 3. Check diagnostic posture & memory
torusguard status

# 4. Formulate minimal surgical candidate patches
torusguard harden

# 5. Apply patches with automatic pre-apply rollback snapshots
torusguard apply

# 6. Generate single-file visual dark-mode HTML dashboard
torusguard report --html

# 7. Export OASIS SARIF v2.1.0 for CI/CD gates
torusguard report --sarif
```

---

## 🌟 Advantages of the `go install` Method

1. **Zero Runtime Dependencies:** Does not require Node.js, npm, or Python.
2. **Instant Startup Time:** Native compiled Go binary starts in sub-millisecond time.
3. **Cross-Language Governance:** Even though it's built in Go, TorusGuard audits JavaScript, TypeScript, Python, Go, and 16+ languages with equal fidelity.
4. **CI/CD Friendly:** Ideal for Go-based GitHub Actions workflows and lightweight Alpine Docker images.

---

## 🔄 Updating TorusGuard

To update to the newest release at any time, re-run:

```bash
go install github.com/githubmofo/TorusGuard/cmd/torusguard@latest
```

---

## 📚 Related Documentation
- [Option 1: npm & npx Usage Guide](option-1-npm.md)
- [Option 2: Build from Source Guide](option-2-source.md)
- [System Architecture](../../README.md#-autonomous-architecture--workflow)
