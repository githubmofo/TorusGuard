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
