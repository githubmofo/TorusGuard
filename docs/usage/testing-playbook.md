# 🧪 TorusGuard Testing Playbook (v2.2.0)

This playbook outlines comprehensive verification procedures across the Go engine, multi-modal Vision OCR, CLI commands, and CI/CD pipelines.

---

## 1. Engine & Unit Testing

### Run Go Unit Tests
```bash
cd TorusGuard
go test -v ./...
# Expected: 100% PASS across scanner, ocr, harden, apply, workspace, etc.
```

### Static Analysis with Go Vet
```bash
go vet ./...
# Expected: Clean exit (0 warnings)
```

### Build Verification
```bash
# On Linux/macOS:
go build -o torusguard ./cmd/torusguard

# On Windows (PowerShell):
go build -o torusguard.exe ./cmd/torusguard
```

---

## 2. Command-Level Verification Suite

### 1. Interactive Command Center
```bash
# Test launching zero-argument interactive center:
./torusguard.exe
# Verify: Renders 75-column menu with options [1] through [10] and [0] Exit.
```

### 2. Workspace Initialization (`init`)
```bash
mkdir -p /tmp/tg-test && cd /tmp/tg-test
echo '{"name": "test-app"}' > package.json
torusguard init
# Verify: .torusguard/ directory is created with active rules and security_report.md
```

### 3. Diagnostic Posture (`status`)
```bash
torusguard status
# Verify: Outputs 75-column posture card with detected stack and active rules.
```

### 4. Hybrid First-Principles Vision OCR (`ocr-scan`)
```bash
# Test A: Auto-discovery across workspace
torusguard ocr-scan
# Verify: Scans all .png, .jpg, .svg in workspace without crashing even if Tesseract is missing.

# Test B: Specific file test
torusguard ocr-scan docs/architecture.png
# Verify: Emits structured finding card if secret signatures exist, or reports 0 leaks found.
```

### 5. Static AST & Taint Audit (`audit`)
```bash
torusguard audit
# Verify: Traverses code ASTs, updates security_report.md, prints calibrated confidence.
```

### 6. Container Hardening Audit (`container`)
```bash
torusguard container
# Verify: Inspects Dockerfile/Compose for root users, sockets, and privileged flags.
```

### 7. Git History Secret Mining (`git-mine`)
```bash
torusguard git-mine
# Verify: Scans commit logs for committed credentials within bounded depth (50 commits).
```

### 8. ReDoS Complexity Scan (`redos`)
```bash
torusguard redos
# Verify: Identifies catastrophic exponential backtracking in regular expressions.
```

### 9. AI & RAG Defense Scan (`ai-guard`)
```bash
torusguard ai-guard
# Verify: Audits system prompts and vector searches for prompt injection / unpartitioned tenants.
```

### 10. Remediation Bounds Enforcement (`harden`)
```bash
# Test valid patch:
cat > test.patch << 'EOF'
--- a/file.go
+++ b/file.go
@@ -1,3 +1,4 @@
 package main
+import "fmt"
 func main() {}
EOF
torusguard harden test.patch
# Verify: Passes Ponytail bounds (1 addition, 0 deletions <= 35/25 limits).
```

### 11. Atomic Patch Application (`apply`)
```bash
torusguard apply --yes test.patch
# Verify: Creates byte-for-byte .bak snapshot in .torusguard/snapshots/ and applies patch.
```

### 12. Instant Rollback (`rollback`)
```bash
torusguard rollback
# Verify: Restores file to previous state from snapshot.
```

### 13. Differential Recheck (`recheck`)
```bash
torusguard recheck
# Verify: Confirms fix closure and marks findings RESOLVED in security_report.md.
```

### 14. Executive Posture Reporting (`report`)
```bash
# Dark-mode HTML report
torusguard report --html
# Verify: Creates report.html (single-file visual dashboard)

# OASIS SARIF v2.1.0 log
torusguard report --sarif
# Verify: Emits valid SARIF JSON conforming to OASIS v2.1.0 specification
```

---

## 3. Security Self-Tests & Invariant Verification

### Path Traversal Defense
```bash
# Attempt to escape workspace via patch
cat > evil.patch << 'EOF'
--- a/../../../etc/passwd
+++ b/../../../etc/passwd
@@ -0,0 +1 @@
+malicious content
EOF
torusguard apply --yes evil.patch
# Verify: Rejected with path traversal error.
```

### Ponytail Churn Limit Enforcement
```bash
# Create patch exceeding 35 additions
python -c "
lines = ['--- a/big.go', '+++ b/big.go', '@@ -0,0 +1,40 @@']
for i in range(40):
    lines.append(f'+line {i}')
print('\n'.join(lines))
" > big.patch
torusguard harden big.patch
# Verify: Rejected with 'exceeds Ponytail Protocol bounds' error.
```

---

## 4. CI/CD Integration Testing

```yaml
# .github/workflows/security.yml
name: TorusGuard Security Gate
on: [push, pull_request]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - name: Run TorusGuard Security Audit
        run: npx torusguard audit
      - name: Run Hybrid OCR Vision Scan
        run: npx torusguard ocr-scan
      - name: Export SARIF Log
        run: npx torusguard report --sarif
      - uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: report.sarif
```
