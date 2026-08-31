# TorusGuard v6 Execution Summary — `nextjs14_actions`

- **Run ID:** `qa-nextjs14`
- **Total Findings Modeled:** 1
- **Confirmed:** 1 | **High Confidence:** 0 | **Needs Review:** 0
- **Root-Cause Clusters:** 1

## Root-Cause Clustering Breakdown

| Cluster ID | Root-Cause Title | Primary Rule | Findings | Files | Hotspot Module | Severity |
|---|---|---|---:|---:|---|---|
| `cluster-idor-scoping` | Insecure Direct Object Reference (IDOR) on Primary Keys | `TG-AUTH-007` | 1 | 1 | `actions.ts` | Critical |


## Next Actions

1. Run `/torusguard harden` to inspect structured remediation bundles.
2. Run `/torusguard apply` to execute Ponytail-governed minimal code modifications.
3. Run `/torusguard recheck` to verify impacted trust boundaries.
