# TorusGuard v6 Execution Summary — `fastapi_pydantic_v2`

- **Run ID:** `qa-fa-v2`
- **Total Findings Modeled:** 1
- **Confirmed:** 1 | **High Confidence:** 0 | **Needs Review:** 0
- **Root-Cause Clusters:** 1

## Root-Cause Clustering Breakdown

| Cluster ID | Root-Cause Title | Primary Rule | Findings | Files | Hotspot Module | Severity |
|---|---|---|---:|---:|---|---|
| `cluster-header-trust` | Untrusted Client Header Trust & Role/Tenant Injection | `TG-AUTH-008` | 1 | 1 | `main.py` | High |


## Next Actions

1. Run `/torusguard harden` to inspect structured remediation bundles.
2. Run `/torusguard apply` to execute Ponytail-governed minimal code modifications.
3. Run `/torusguard recheck` to verify impacted trust boundaries.
