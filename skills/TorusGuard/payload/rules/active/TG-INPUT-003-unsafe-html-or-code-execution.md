# TG-INPUT-003: Unsafe HTML Rendering or Code Execution

## Severity
High

## Applies To
- Server-side rendering pipelines
- Rich text/comment rendering features
- Template engines and markdown-to-HTML converters
- Dynamic expression evaluators and script execution utilities

## Why It Matters
When untrusted content is rendered as HTML without sanitization, attackers can inject scripts and trigger stored or reflected XSS.
When untrusted input reaches evaluators such as `eval`, `Function`, or shell execution helpers, remote code execution and server compromise become possible.
These flaws frequently lead to session theft, account takeover, and full application compromise.

## What TorusGuard Looks For
- Use of dangerous rendering APIs such as `innerHTML`, `dangerouslySetInnerHTML`, or unsanitized template output.
- Markdown or rich text conversion with unsafe options enabled.
- Invocation of `eval`, `new Function`, VM contexts, or command execution with user-controlled fragments.
- Security filters that rely only on regex stripping of script tags.
- User content stored and later rendered in privileged admin views.

## Unsafe Example
```js
app.post("/api/notes/preview", (req, res) => {
  const body = req.body.content;

  // Stored then rendered unsafely
  const html = `<article>${body}</article>`;
  res.send(html);
});

app.post("/api/calc", (req, res) => {
  const expression = req.body.expression;

  // User controls executed code
  const result = eval(expression);
  res.json({ ok: true, result });
});
```

## Safe Example
```js
import sanitizeHtml from "sanitize-html";

app.post("/api/notes/preview", (req, res) => {
  const content = String(req.body.content || "");
  const safe = sanitizeHtml(content, {
    allowedTags: ["p", "b", "i", "strong", "em", "ul", "ol", "li", "a", "code", "pre"],
    allowedAttributes: { a: ["href", "title"] },
    allowedSchemes: ["http", "https", "mailto"]
  });

  res.send(`<article>${safe}</article>`);
});

app.post("/api/calc", (req, res) => {
  const op = String(req.body.op || "");
  const left = Number(req.body.left);
  const right = Number(req.body.right);

  if (!Number.isFinite(left) || !Number.isFinite(right)) {
    return res.status(400).json({ ok: false, error: "Invalid numeric input" });
  }

  const operations = {
    add: (a, b) => a + b,
    sub: (a, b) => a - b,
    mul: (a, b) => a * b,
    div: (a, b) => (b === 0 ? null : a / b)
  };

  if (!operations[op]) return res.status(400).json({ ok: false, error: "Unsupported operation" });
  res.json({ ok: true, result: operations[op](left, right) });
});
```

## Remediation
1. Treat all user-controlled text as untrusted until sanitized for the target context.
2. Use maintained HTML sanitizers with explicit allowlists for tags and attributes.
3. Ban runtime code execution functions (`eval`, `Function`, shell interpolation) in request paths.
4. Replace expression execution with constrained allowlisted operations.
5. Enforce contextual output encoding in templates and frontend rendering layers.
6. Add CSP and defense-in-depth controls, but do not treat them as primary mitigation.

## Verification
- Submit payloads containing event handlers, script tags, and `javascript:` URLs.
- Confirm rendered output strips unsafe elements and attributes.
- Attempt expression payloads like `process.env` and verify they are rejected.
- Run security tests for stored and reflected rendering flows, including admin pages.
- Ensure static analysis flags prohibited runtime execution APIs.

## False Positives and Exceptions
- Trusted, static CMS content curated by privileged staff may allow richer HTML if isolated and sanitized by policy.
- Template literals are not inherently unsafe; only sinks that interpret HTML/code create risk.
- Sandboxed code execution environments still require strict resource and capability restrictions.

## Related Rules
- [TG-INPUT-001](./TG-INPUT-001-missing-server-validation.md)
- [TG-INPUT-002](./TG-INPUT-002-raw-sql-concatenation.md)
- [TG-AUTH-004](./TG-AUTH-004-insecure-session-cookie.md)
