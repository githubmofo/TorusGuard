# Intentionally Vulnerable Example: SQLAlchemy Fixture
> **WARNING:** This project exists only to test and demonstrate TorusGuard guidance. Do not deploy it, expose it to the internet, reuse its security patterns, or add real credentials. All secrets, users, payment values, and tokens are fake and nonfunctional.

---

## 🎯 Educational Purpose
Demonstrates common SQLAlchemy data-layer flaws:
1. **`TG-INPUT-003`**: Raw SQL injection using f-strings in `text()`.
2. **`TG-AUTH-007`**: Order lookup query missing user ownership filter (IDOR).
3. **`TG-AUTH-006`**: Bulk update passing raw user-controlled dictionary directly to `.update()`.

See [fixes.md](fixes.md) and [../sqlalchemy-hardened/](../sqlalchemy-hardened/) for the hardened counterpart.
