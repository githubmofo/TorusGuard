# Django Rule Verification Matrix (TorusGuard v0.4.0)

| Rule ID | Rule Title | Test Target File | Detection Check | Expected Result | Confidence |
|---|---|---|---|---|:---:|
| `TG-SEC-001` | Hardcoded Secrets | `config/settings.py` | `SECRET_KEY = 'django-insecure-...'` | Flagged as Hardcoded Secret | Confirmed |
| `TG-PLATFORM-003` | Insecure Debug Mode | `config/settings.py` | `DEBUG = True` without environment guard | Flagged in Production Config | Confirmed |
| `TG-AUTH-007` | Object Ownership IDOR | `accounts/views.py` | `Document.objects.get(id=doc_id)` without user filter | Flagged as IDOR vulnerability | Confirmed |
| `TG-AUTH-006` | Mass Assignment | `accounts/forms.py` | `fields = '__all__'` on `ModelForm` | Flagged as Mass Assignment Risk | Confirmed |
| `TG-CACHE-001` | Sensitive Cache Missing | `accounts/views.py` | Profile view lacks `@never_cache` decorator | Flagged as Cache Exposure | Confirmed |
| `TG-CSRF-001` | CSRF Middleware Check | `config/settings.py` | `CsrfViewMiddleware` presence | Verified Active | Confirmed |
