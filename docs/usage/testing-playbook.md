# TorusGuard Testing Playbook

## Running Tests

### Go Unit Tests

```bash
cd TorusGuard
go test ./...
```

### Go Vet (Static Analysis)

```bash
go vet ./...
```

### Build Verification

```bash
go build -o torusguard.exe ./cmd/torusguard
```

## Command-Level Testing

### 1. Init

```bash
# Create a temp directory and initialize TorusGuard
mkdir /tmp/test-project && cd /tmp/test-project
echo '{"name": "test"}' > package.json
torusguard init
# Verify: .torusguard/ directory should be created with rules/ and schemas/
```

### 2. Status

```bash
torusguard status
# Verify: Should display detected stack and posture overview
```

### 3. Audit

```bash
torusguard audit
# Verify: security_report.md should be created/updated with findings
```

### 4. Harden

```bash
# Create a test patch
cat > test.patch << 'EOF'
--- a/file.go
+++ b/file.go
@@ -1,3 +1,4 @@
 package main
+import "fmt"
 func main() {}
EOF
torusguard harden test.patch
# Verify: Should pass Ponytail bounds (1 addition, 0 deletions)
```

### 5. Apply

```bash
torusguard apply --yes test.patch
# Verify: .torusguard/snapshots/ should contain a .bak file
# Verify: The patch should be applied to the target file
```

### 6. Rollback

```bash
torusguard rollback
# Verify: The target file should be restored from the snapshot
```

### 7. Report

```bash
torusguard report --sarif
# Verify: report.sarif should contain valid JSON with findings

torusguard report --html
# Verify: report.html should contain a dark-mode HTML dashboard
```

### 8. Authorize

```bash
torusguard authorize
# Verify: .torusguard/auth.json should contain a cryptographic token with TTL
```

### 9. Web Validate

```bash
# Start a local server first, then:
torusguard web-validate
# Verify: Should report HTTP status code and check for Content-Security-Policy header
# If no server is running, should gracefully report "Could not reach target application"
```

### 10. Exploit Check

```bash
torusguard exploit-check
# Verify: Should report whether the application handled inert SQL injection payload gracefully
```

## Security Self-Tests

### Path Traversal Defense

```bash
# Create a malicious patch targeting outside the workspace
cat > evil.patch << 'EOF'
--- a/../../../etc/passwd
+++ b/../../../etc/passwd
@@ -0,0 +1 @@
+malicious content
EOF
torusguard apply --yes evil.patch
# Verify: Should fail with "target file does not exist" or path traversal error
```

### Ponytail Bounds Enforcement

```bash
# Create a patch exceeding 35 additions
python -c "
lines = ['--- a/big.go', '+++ b/big.go', '@@ -0,0 +1,40 @@']
for i in range(40):
    lines.append(f'+line {i}')
print('\n'.join(lines))
" > big.patch
torusguard harden big.patch
# Verify: Should fail with "exceeds Ponytail Protocol bounds"
```

## CI Integration

```yaml
# .github/workflows/security.yml
name: TorusGuard Security Gate
on: [push, pull_request]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '1.25'
      - run: go build -o torusguard ./cmd/torusguard
      - run: ./torusguard init
      - run: ./torusguard audit
      - run: ./torusguard report --sarif
      - uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: report.sarif
```
