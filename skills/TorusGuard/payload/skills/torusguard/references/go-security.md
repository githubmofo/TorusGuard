# TorusGuard Skill Reference: Go Security

> **Loaded When:** A project is identified as a Go application (`go.mod`, `go.sum`, or Go source files detected).

---

## 🛡️ Key Inspection Areas & Rules

### 1. Database & SQL Injection
* `TG-INPUT-002`: Ensure raw queries use parameterized placeholders (`?`, `$1`), never `fmt.Sprintf` or string concatenation.
* `TG-DB-004`: Enforce tenant isolation in GORM queries (`db.Where("tenant_id = ?", tenantID)`).

### 2. TLS & Network Security
* `TG-DIFF-001`: Prohibit `InsecureSkipVerify: true` in `tls.Config`. Always use valid root CA pools.
* `TG-SSRF-001`: Validate outbound URLs before issuing `http.Get` or `http.Post`.

### 3. Concurrency & Goroutine Safety
* `TG-BIZ-001`: Ensure context cancellation propagation (`ctx.Done()`) to prevent goroutine leaks.
* Use mutexes or channels to prevent data races on shared state.

### 4. Input Validation & Path Traversal
* `TG-INPUT-006`: Sanitize file paths with `filepath.Clean` and check `strings.HasPrefix(cleanPath, baseDir)`.

---

## 🛠️ Safe Patterns Summary

```go
// Safe Parameterized Query
row := db.QueryRowContext(ctx, "SELECT id, email FROM users WHERE id = ? AND tenant_id = ?", userID, tenantID)

// Safe GORM Scoping
var invoice Invoice
result := db.Where("id = ? AND tenant_id = ?", invoiceID, currentTenantID).First(&invoice)

// Safe TLS Client
tlsConfig := &tls.Config{
    MinVersion: tls.VersionTLS13,
}
client := &http.Client{Transport: &http.Transport{TLSClientConfig: tlsConfig}}
```
