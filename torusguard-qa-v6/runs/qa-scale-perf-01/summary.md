# TorusGuard v6 Execution Summary — `perf-bench`

- **Run ID:** `qa-scale-perf-01`
- **Total Findings Modeled:** 5
- **Confirmed:** 5 | **High Confidence:** 0 | **Needs Review:** 0
- **Root-Cause Clusters:** 1

## Root-Cause Clustering Breakdown

| Cluster ID | Root-Cause Title | Primary Rule | Findings | Files | Hotspot Module | Severity |
|---|---|---|---:|---:|---|---|
| `cluster-tenant-isolation` | Missing Multi-Tenant Query Scoping & Model Isolation | `TG-DB-004` | 5 | 5 | `apps/service_4` | High |


## Next Actions

1. Run `/torusguard harden` to inspect structured remediation bundles.
2. Run `/torusguard apply` to execute Ponytail-governed minimal code modifications.
3. Run `/torusguard recheck` to verify impacted trust boundaries.
