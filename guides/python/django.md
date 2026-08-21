# Django Security Guide (TorusGuard v0.4.0)

> **Scope:** Security standards and hardening guidance for Django applications. Focuses on built-in security features, production settings, ORM safety, object-level authorization, CSRF defense, and file upload boundaries.

---

## 🔍 Scope and Detection
TorusGuard identifies Django projects by detecting `manage.py`, `wsgi.py`, `asgi.py`, `settings.py`, or `django` in dependency manifests.

---

## ⚙️ 1. Settings & Production Deployment

Django includes robust production security mechanisms that must be explicitly configured for non-development environments.

### Critical Production Settings
```python
# settings.py - Production Configuration
import os
from pathlib import Path

# 1. Disable Debug Mode in Production (TG-PLATFORM-003)
DEBUG = False

# 2. Secret Key from Environment (TG-SEC-001)
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY and not DEBUG:
    raise RuntimeError("DJANGO_SECRET_KEY must be set in production.")

# 3. Explicit Allowed Hosts (TG-PLATFORM-001)
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "example.com,api.example.com").split(",")

# 4. HTTPS and Cookie Security Flags
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

# 5. HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# 6. Content Security & XSS Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
```

*Verification Command:*
```bash
python manage.py check --deploy
```
*(Note: `manage.py check --deploy` is a helpful baseline check, but does not substitute for full configuration review.)*

---

## 🛡️ 2. CSRF Protection (`TG-CSRF-001`)

Django includes built-in CSRF protection enabled by default via `django.middleware.csrf.CsrfViewMiddleware`.

### Safe Patterns
* Ensure `'django.middleware.csrf.CsrfViewMiddleware'` is present in `MIDDLEWARE`.
* In all template POST forms, include `{% csrf_token %}`.
* For AJAX requests, read the CSRF cookie or send the `X-CSRFToken` header.
* **Avoid** using `@csrf_exempt` on session-authenticated routes. If building an unauthenticated external webhook handler, verify signatures manually rather than relying solely on `@csrf_exempt`.

---

## 🗄️ 3. Django ORM & Raw SQL Safety (`TG-INPUT-003`, `TG-DB-001`)

Django's ORM automatically parameterizes SQL queries. However, raw SQL methods require caution.

### ❌ Unsafe Pattern: SQL String Concatenation
```python
# VULNERABLE: Direct string interpolation into raw SQL
email = request.POST.get("email")
users = User.objects.raw(f"SELECT * FROM auth_user WHERE email = '{email}'")
```

### ✅ Safe Pattern: Parameterized Queries or ORM Lookups
```python
# SAFE: Use ORM queryset lookups
email = request.POST.get("email")
users = User.objects.filter(email=email)

# SAFE: If raw SQL is strictly required, use parameters list/dict
users = User.objects.raw("SELECT * FROM auth_user WHERE email = %s", [email])
```

---

## 👤 4. Object Ownership & Authorization (`TG-AUTH-007`)

A numeric primary key in a URL must never be queried without filtering by the authenticated user.

### ❌ Unsafe Pattern (IDOR)
```python
# VULNERABLE: Any logged-in user can view document #42 by guessing the ID
@login_required
def view_document(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)
    return render(request, "doc.html", {"doc": doc})
```

### ✅ Safe Pattern (Ownership-Scoped Queryset)
```python
# SAFE: Scope lookup strictly to the authenticated user's records
@login_required
def view_document(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id, owner=request.user)
    return render(request, "doc.html", {"doc": doc})
```

---

## 📝 5. Forms & Mass Assignment (`TG-AUTH-006`)

`ModelForm` classes must explicitly define allowed editable fields.

### ❌ Unsafe Pattern
```python
# VULNERABLE: Allows client to submit 'is_staff' or 'is_superuser'
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'  # ❌ Dangerous mass assignment
```

### ✅ Safe Pattern
```python
# SAFE: Explicit whitelist of safe fields
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio']  # ✅ Safe whitelist
```

---

## 📂 6. File Uploads & Media Storage (`TG-INPUT-004`)

* **Storage:** Store user uploads in dedicated object storage (AWS S3, Google Cloud Storage) or outside the web server's executable document root.
* **File Validation:** Validate allowed extensions, file size, and MIME content.
* **Execution Prevention:** Ensure the web server (Nginx/Apache) does not execute PHP/Python/CGI scripts in the `MEDIA_ROOT` directory.

---

## ⚡ 7. Cache & Sensitive Responses (`TG-CACHE-001`)

Use `@never_cache` on sensitive user views (billing, profile, reset password) to prevent caching in public intermediate proxies.

```python
from django.views.decorators.cache import never_cache

@never_cache
@login_required
def billing_details(request):
    return render(request, "billing.html", {"billing": request.user.billing_profile})
```

---

## 📋 Manual Review Checklist for Django

- [ ] `DEBUG` is set to `False` in production environments.
- [ ] `SECRET_KEY` is loaded from a secure environment variable and never committed.
- [ ] `ALLOWED_HOSTS` contains only explicit domain names (no wildcard `*` with credentials).
- [ ] `CsrfViewMiddleware` is enabled in `MIDDLEWARE`.
- [ ] All `ModelForm` definitions use explicit `fields` arrays rather than `'__all__'`.
- [ ] All object lookups by numeric ID filter by `request.user` or tenant ID.
- [ ] The Django Admin path is hardened or restricted via IP allowlist / 2FA.
- [ ] File uploads validate extension, size, and use dedicated storage.
