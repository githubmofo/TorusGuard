# Hardened SQLAlchemy Reference Implementation

> **Purpose:** Reference implementation demonstrating TorusGuard-compliant parameterized queries, ownership-scoped filters, and safe update boundaries in SQLAlchemy.

---

## 🛡️ Applied Security Controls

1. **Named Parameter Binding (`TG-INPUT-003`):** Raw SQL constructs use `:param` bindings.
2. **Tenant Ownership Scoping (`TG-AUTH-007`):** Query constructs include `user_id == current_user_id` predicates.
3. **Explicit Field Allowlist (`TG-AUTH-006`):** Updates filter client dictionaries against predefined allowlists.

See [fixes.md](fixes.md) for details.
