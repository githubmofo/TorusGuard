# TorusGuard Skill Reference: SQLAlchemy Security

> **Loaded When:** Project uses `sqlalchemy` dependencies or imports.

---

## 🛡️ Key Inspection Areas & Rules

### 1. SQL Injection in Raw Query Clauses
* `TG-INPUT-003`: Search for `text(f"...")`, `text("..." + ...)`, or `.format()` inside `text()` constructs. Ensure parameter mapping `text("... WHERE col = :val")` is used.

### 2. Tenant Scoping & Object Ownership
* `TG-AUTH-007`: Verify queries on tenant-isolated tables include tenant/user ID predicates in `.filter()` or `.filter_by()`.

### 3. Mass Assignment via Bulk Updates
* `TG-AUTH-006`: Inspect `.update(dict)` calls to ensure input dictionaries are filtered against permitted field allowlists.
