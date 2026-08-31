# TorusGuard v6 Execution Summary — `sqlalchemy-multitenant`

- **Run ID:** `qa-apply-sqlalchemy-multitenant`
- **Total Findings Modeled:** 1
- **Confirmed:** 1 | **High Confidence:** 0 | **Needs Review:** 0
- **Root-Cause Clusters:** 1

## Root-Cause Clustering Breakdown

| Cluster ID | Root-Cause Title | Primary Rule | Findings | Files | Hotspot Module | Severity |
|---|---|---|---:|---:|---|---|
| `cluster-tenant-isolation` | Missing Multi-Tenant Query Scoping & Model Isolation | `TG-DB-004` | 1 | 1 | `queries.py` | High |


## Next Actions

1. Run `/torusguard harden` to inspect structured remediation bundles.
2. Run `/torusguard apply` to execute Ponytail-governed minimal code modifications.
3. Run `/torusguard recheck` to verify impacted trust boundaries.
