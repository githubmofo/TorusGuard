# TorusGuard v6 Execution Summary — `complex-monorepo`

- **Run ID:** `qa-scale-monorepo-01`
- **Total Findings Modeled:** 5
- **Confirmed:** 0 | **High Confidence:** 0 | **Needs Review:** 0
- **Root-Cause Clusters:** 5

## Root-Cause Clustering Breakdown

| Cluster ID | Root-Cause Title | Primary Rule | Findings | Files | Hotspot Module | Severity |
|---|---|---|---:|---:|---|---|
| `cluster-tenant-isolation` | Missing Multi-Tenant Query Scoping & Model Isolation | `TG-DB-004` | 1 | 1 | `apps/django_core` | High |
| `cluster-ssrf-network` | Unvalidated Outbound HTTP Requests & Network Boundary Leakage | `TG-SSRF-001` | 1 | 1 | `apps/fastapi_service` | High |
| `cluster-webhook-auth` | Unverified Inbound Webhook Signatures & Replay Vulnerability | `TG-WEBHOOK-001` | 1 | 1 | `apps/flask_webhook` | High |
| `cluster-path-traversal` | Unsafe File Upload Storage & Path Traversal Boundaries | `TG-INPUT-006` | 1 | 1 | `services/core` | High |
| `cluster-supply-001` | Systemic Unpinned GitHub Action in Production Pipeline Issues | `TG-SUPPLY-001` | 1 | 1 | `infra/.github` | Medium |


## Next Actions

1. Run `/torusguard harden` to inspect structured remediation bundles.
2. Run `/torusguard apply` to execute Ponytail-governed minimal code modifications.
3. Run `/torusguard recheck` to verify impacted trust boundaries.
