# TorusGuard Skill Reference: Rust Security

> **Loaded When:** A project is identified as a Rust application (`Cargo.toml` or `.rs` files detected).

---

## 🛡️ Key Inspection Areas & Rules

### 1. Memory Safety & Unsafe Blocks
* `TG-INPUT-003`: Audit and restrict `unsafe { ... }` blocks. Must include a `// SAFETY:` rationale comment.
* Never disable standard borrow checker lints via `#![allow(unsafe_code)]`.

### 2. Database & SQL Queries
* `TG-INPUT-002`: Use compile-time checked `sqlx::query!` or Diesel query builder methods.
* `TG-DB-004`: Enforce tenant filtering in queries (`filter(tenant_id.eq(current_tenant_id))`).

### 3. Outbound Requests & TLS
* `TG-DIFF-001`: Prohibit `danger_accept_invalid_certs(true)` in `reqwest::ClientBuilder`.
* `TG-SSRF-001`: Enforce IP allowlists before dispatching network calls.

---

## 🛠️ Safe Patterns Summary

```rust
// Safe sqlx Parameterized Query
let user = sqlx::query_as!(
    User,
    "SELECT id, email FROM users WHERE id = $1 AND tenant_id = $2",
    user_id,
    current_tenant_id
)
.fetch_one(&pool)
.await?;

// Safe reqwest Client (Strict TLS)
let client = reqwest::Client::builder()
    .timeout(std::time::Duration::from_secs(10))
    .build()?;
```
