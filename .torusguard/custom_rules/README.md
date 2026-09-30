# TorusGuard Custom Security Rules (TG-QL)

Place your custom declarative security rules (`.yaml`, `.yml`, or `.json`) in this directory. TorusGuard compiles and evaluates them dynamically on every audit, review, and MCP invocation with zero Go recompilation.

## Example Custom Rule: `admin-auth-guard.yaml`

```yaml
id: TG-CUSTOM-001
severity: HIGH
languages: [.js, .ts, .py, .go]
pattern: "app.post('/api/admin/$PATH', $HANDLER)"
not_inside: "requireAdminAuth"
description: "Administrative API endpoint declared without mandatory requireAdminAuth middleware"
suggested_fix: "Wrap route handler with requireAdminAuth: app.post('/api/admin/$PATH', requireAdminAuth, $HANDLER)"
```

## Supported Fields:
- `id`: Unique rule identifier (e.g., `TG-CUSTOM-001`)
- `severity`: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, or `INFO`
- `languages`: Array of target file extensions (e.g., `[.js, .ts, .py, .go]`)
- `pattern`: Code pattern with metavariables (`$VAR`, `$PATH`, `$HANDLER`, `...`)
- `not_inside`: Guard or sanitizer that negates the finding if present
- `description`: Plain-English explanation of why this is a risk
- `suggested_fix`: Prescriptive remediation instruction
