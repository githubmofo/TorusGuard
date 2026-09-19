# TG-PLATFORM-004: Missing Request Size Limits

## Severity

Medium

## Applies To

- JSON body parsers in API servers
- Multipart upload handlers (`multer`, `busboy`, `formidable`)
- Reverse proxies and gateways handling inbound body buffering
- GraphQL endpoints accepting deeply nested or large payloads
- Webhook endpoints receiving internet-originated request bodies

## Why It Matters

Unlimited request body size enables straightforward resource exhaustion.
Attackers can submit oversized payloads to consume memory, CPU, and I/O.
Large bodies also amplify parser overhead before business logic runs.
This can degrade service availability and increase infrastructure cost.
Body limits are a foundational availability control.

## What TorusGuard Looks For

- `express.json()` or equivalent parser used without `limit`
- Multipart middleware configured without `fileSize`/part-count constraints
- Reverse proxy body size defaults left unconfigured for production
- Endpoints accepting large payloads without authentication or quotas
- Missing early rejection behavior (`413 Payload Too Large`)
- No per-route differentiation (tiny webhook route shares unlimited global limits)

## Unsafe Example

```ts
import express from "express";
import multer from "multer";

const app = express();
const upload = multer(); // no limits

app.use(express.json()); // no limit
app.post("/api/upload", upload.single("file"), async (req, res) => {
  await storeFile(req.file);
  res.json({ ok: true });
});
```

## Safe Example

```ts
import express from "express";
import multer from "multer";

const app = express();
const upload = multer({
  limits: {
    fileSize: 5 * 1024 * 1024,
    files: 1,
    fields: 20
  }
});

app.use(express.json({ limit: "1mb" }));
app.use(express.urlencoded({ extended: false, limit: "256kb" }));

app.post("/api/upload", upload.single("file"), async (req, res) => {
  await storeFile(req.file);
  res.json({ ok: true });
});
```

## Remediation

1. Set explicit global parser limits for JSON, form, and text payloads.
2. Apply stricter route-level limits for sensitive or low-bandwidth endpoints.
3. Configure multipart middleware with file size, file count, and field limits.
4. Mirror limits at gateway/proxy layer for early rejection and cost control.
5. Return consistent `413` responses and avoid expensive post-parse handling.
6. Require auth and quotas for routes that legitimately need larger bodies.
7. Add depth/complexity controls for GraphQL or nested JSON structures.
8. Monitor rejected payload metrics and adjust limits based on observed traffic.

## Verification

- Submit oversized JSON/form/multipart payloads and confirm `413` behavior.
- Verify limits are enforced consistently across app and edge layers.
- Confirm normal legitimate payloads still succeed.
- Stress-test endpoints to ensure parser memory remains bounded.
- Validate logs and metrics capture payload-limit rejections cleanly.

## False Positives and Exceptions

- Internal batch ingestion endpoints on private networks with strict contracts
- Dedicated large-upload services with chunked protocols and isolated capacity
- Temporary migration windows requiring higher limits with compensating controls
- Routes where limits are enforced upstream and app parser never sees large bodies

## Related Rules

- `TG-RATE-003-unbounded-resource-consumption.md`
- `TG-RATE-002-unlimited-public-write-endpoint.md`
- `TG-INPUT-004-unrestricted-file-upload.md`
