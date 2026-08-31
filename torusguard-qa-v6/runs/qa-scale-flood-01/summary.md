# TorusGuard v6 Execution Summary — `high-density-flood`

- **Run ID:** `qa-scale-flood-01`
- **Total Findings Modeled:** 250
- **Confirmed:** 200 | **High Confidence:** 50 | **Needs Review:** 0
- **Root-Cause Clusters:** 3

## Root-Cause Clustering Breakdown

| Cluster ID | Root-Cause Title | Primary Rule | Findings | Files | Hotspot Module | Severity |
|---|---|---|---:|---:|---|---|
| `cluster-tenant-isolation` | Missing Multi-Tenant Query Scoping & Model Isolation | `TG-DB-004` | 120 | 15 | `services/api` | High |
| `cluster-path-traversal` | Unsafe File Upload Storage & Path Traversal Boundaries | `TG-INPUT-006` | 80 | 10 | `services/uploads` | High |
| `cluster-header-trust` | Untrusted Client Header Trust & Role/Tenant Injection | `TG-AUTH-008` | 50 | 5 | `services/gateway` | High |


## Next Actions

1. Run `/torusguard harden` to inspect structured remediation bundles.
2. Run `/torusguard apply` to execute Ponytail-governed minimal code modifications.
3. Run `/torusguard recheck` to verify impacted trust boundaries.
