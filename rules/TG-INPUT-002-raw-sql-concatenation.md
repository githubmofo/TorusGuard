# TG-INPUT-002: Raw SQL Concatenation

## Severity
Critical

## Applies To
- Backend services that execute SQL queries
- Scripts and cron jobs that build dynamic SQL
- Data export/reporting endpoints with filters and sorting
- Administrative tooling with direct database access

## Why It Matters
Concatenating untrusted input into SQL statements allows SQL injection, one of the highest-impact application vulnerabilities.
Successful exploitation can expose sensitive records, bypass authentication checks, modify or delete data, and in some environments execute database-level administrative operations.
Even read-only endpoints can become a pivot for full data exfiltration when query construction is unsafe.

## What TorusGuard Looks For
- String interpolation or concatenation inside SQL query text using request-derived data.
- Dynamic `WHERE`, `ORDER BY`, `LIMIT`, or table-name fragments assembled from raw user input.
- Use of low-level query APIs without bind parameters.
- Sanitization-only approaches (replace/escape) used instead of parameterization.
- Unsafe helper functions that return query strings rather than query templates plus values.

## Unsafe Example
```js
app.get("/api/orders", async (req, res) => {
  const customerId = req.query.customerId;
  const sort = req.query.sort || "created_at DESC";

  // Both customerId and sort are attacker-controlled
  const sql =
    "SELECT id, total, created_at FROM orders " +
    "WHERE customer_id = '" + customerId + "' " +
    "ORDER BY " + sort;

  const rows = await db.query(sql);
  res.json({ ok: true, orders: rows });
});
```

## Safe Example
```js
const SORT_COLUMNS = new Map([
  ["newest", "created_at DESC"],
  ["oldest", "created_at ASC"],
  ["total_high", "total DESC"],
  ["total_low", "total ASC"]
]);

app.get("/api/orders", async (req, res) => {
  const customerId = String(req.query.customerId || "");
  const sortKey = String(req.query.sort || "newest");
  const sortSql = SORT_COLUMNS.get(sortKey);

  if (!sortSql || !/^[a-f0-9-]{36}$/.test(customerId)) {
    return res.status(400).json({ ok: false, error: "Invalid query parameters" });
  }

  const sql = `
    SELECT id, total, created_at
    FROM orders
    WHERE customer_id = $1
    ORDER BY ${sortSql}
  `;

  const rows = await db.query(sql, [customerId]);
  res.json({ ok: true, orders: rows });
});
```

## Remediation
1. Replace all string-built SQL with parameterized queries or prepared statements.
2. Bind user input as values, never as SQL syntax fragments.
3. For dynamic sorting/filtering, map user options to fixed allowlisted SQL snippets.
4. Restrict database account privileges to least privilege to reduce blast radius.
5. Add static analysis and code review checks that ban raw concatenated SQL.
6. Cover injection payloads in automated tests for every query endpoint.

## Verification
- Search for query construction using template interpolation with request variables.
- Attempt payloads such as `' OR '1'='1` and confirm they are treated as literal values.
- Verify sort/filter options accept only predefined keys.
- Review database logs for rejected malformed statements and suspicious patterns.
- Confirm all DB access layers support parameter binding and are consistently used.

## False Positives and Exceptions
- Hardcoded SQL strings with no untrusted input are generally safe.
- Migration files may contain dynamic SQL for schema operations; these are acceptable if not user-influenced.
- Internal ETL code can still be vulnerable if source data is not trusted; do not auto-exempt.

## Related Rules
- [TG-INPUT-001](./TG-INPUT-001-missing-server-validation.md)
- [TG-INPUT-003](./TG-INPUT-003-unsafe-html-or-code-execution.md)
- [TG-AUTH-003](./TG-AUTH-003-missing-object-authorization.md)
