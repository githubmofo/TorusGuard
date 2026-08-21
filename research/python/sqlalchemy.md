# SQLAlchemy Security Research Notes (TorusGuard v0.4.0)

## Research Findings
- **Raw SQL Pitfalls:** ORM queries are parameterized by default, but developers often revert to `text(f"SELECT ... WHERE col = '{val}'")` for complex filtering, creating SQL injection vulnerabilities.
- **Update Mapping:** Unfiltered client dictionaries passed to `.update(dict)` bypass column safety boundaries.
- **Tenant Isolation:** Multi-tenant schemas must enforce tenant/user filters across all query boundaries.
