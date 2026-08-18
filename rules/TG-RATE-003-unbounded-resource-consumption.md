# TG-RATE-003: Unbounded Resource Consumption

## Severity

High

## Applies To

- Search and reporting endpoints with user-controlled pagination or filters
- File generation/export endpoints (CSV, PDF, ZIP)
- Media processing, image transforms, and AI inference routes
- Query parameters controlling recursion depth, fan-out, or batch size
- Any endpoint that triggers heavy DB, CPU, memory, or outbound calls

## Why It Matters

Not all abuse is about raw request count.
A single request can be dangerously expensive when workload is unbounded.
Attackers can force large scans, huge responses, or runaway processing jobs.
This can produce denial-of-service and significant infrastructure cost.
Legitimate users also suffer from latency and instability during abuse events.

## What TorusGuard Looks For

- Missing upper bounds on `limit`, `pageSize`, `depth`, `expand`, or `batchSize`
- Export endpoints that allow entire dataset extraction in one request
- Image/AI endpoints with unrestricted dimensions, duration, or token budgets
- No request timeouts, execution budgets, or cancellation support
- DB queries lacking pagination while returning client-controlled result sizes
- Loops over user-provided ranges without hard caps

## Unsafe Example

```ts
app.get("/api/reports/users", async (req, res) => {
  const limit = Number(req.query.limit ?? 1000);
  const users = await db.user.findMany({
    where: { active: true },
    take: limit
  });
  res.json({ users });
});

app.post("/api/export", async (req, res) => {
  const rows = await db.orders.findMany(); // full table scan/export
  const csv = await toCsv(rows);
  res.type("text/csv").send(csv);
});
```

## Safe Example

```ts
const MAX_REPORT_LIMIT = 100;
const MAX_EXPORT_ROWS = 5000;

app.get("/api/reports/users", async (req, res) => {
  const requested = Number(req.query.limit ?? 25);
  const limit = Math.min(Math.max(requested, 1), MAX_REPORT_LIMIT);
  const users = await db.user.findMany({
    where: { active: true },
    take: limit
  });
  res.json({ users, limit });
});

app.post("/api/export", async (req, res) => {
  const rows = await db.orders.findMany({ take: MAX_EXPORT_ROWS });
  const csv = await toCsv(rows);
  res.type("text/csv").send(csv);
});
```

## Remediation

1. Define explicit upper bounds for all user-controlled workload parameters.
2. Clamp values server-side even when frontend already validates inputs.
3. Require pagination for list endpoints and deny unbounded bulk reads.
4. Add compute and execution guardrails (timeouts, cancellation, queue budgets).
5. Cap export size and move large jobs to async pipelines with quotas.
6. Set sane payload and response size thresholds per route type.
7. Add observability for p95/p99 cost, timeout, and reject rates by endpoint.
8. Load-test abuse scenarios and tune bounds before production rollout.

## Verification

- Request extreme `limit`/`depth` values and verify clamping behavior.
- Confirm oversized exports are blocked or converted to queued async jobs.
- Measure endpoint latency under stress and verify no runaway degradation.
- Validate timeout and cancellation behavior for long-running workloads.
- Ensure alerting fires when expensive request patterns spike.

## False Positives and Exceptions

- Internal analytics jobs running on private networks with dedicated quotas
- One-off administrative endpoints gated by strong auth and network controls
- Batch endpoints with strict signed-client access and audited operator use
- Synthetic benchmarks intentionally disabling caps in isolated environments

## Related Rules

- `TG-RATE-001-unlimited-auth-endpoint.md`
- `TG-RATE-002-unlimited-public-write-endpoint.md`
- `TG-PLATFORM-004-missing-request-size-limits.md`
- `TG-INPUT-001-missing-server-validation.md`
