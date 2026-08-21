# TorusGuard Test Verification Matrix

| Rule ID | Stack / Target | Evidence Checked | Automated / Manual | False Positive Risk | Action |
|---|---|---|---|---|---|
| `TG-CSRF-001` | NodeGoat / Django / Flask | `CsrfViewMiddleware` / `CSRFProtect` | Static config + route inspect | No | Keep |
| `TG-CACHE-001` | NodeGoat / Django | `@never_cache` / `Cache-Control` header | Static + response header check | Low | Clarified |
| `TG-SUPPLY-001` | Python / Node.js | `poetry.lock` / `package-lock.json` | Manifest vs lockfile detection | No | Keep |
| `TG-SUPPLY-002` | Python / Node.js | `pip-audit` / `npm audit` | Ecosystem tool review | Low | Keep |
| `TG-SSRF-001` | FastAPI / Node.js | Outbound request destination validation | Static + IP address resolution | Low | Keep |
| `TG-AUTH-006` | DRF / Django / FastAPI | Serializer fields / ModelForm / Pydantic | Static schema review | No | Keep |
| `TG-AUTH-007` | Django / DRF / FastAPI / Flask | Numeric ID query ownership filters | Static AST & query filter review | Low | Keep |
| `TG-INPUT-003` | SQLAlchemy / Django | Raw SQL f-string vs param binding | Static query construct review | No | Keep |
| `TG-INPUT-004` | Flask / Django | `secure_filename()` / extension allowlists | Static upload handler review | No | Keep |
| `TG-WEBHOOK-001` | FastAPI / Node.js | HMAC raw body signature comparison | Static header & hash inspect | No | Keep |
