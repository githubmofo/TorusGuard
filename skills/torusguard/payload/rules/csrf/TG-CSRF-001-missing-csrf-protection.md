# TG-CSRF-001: Missing CSRF Protection

## Severity
Critical. State-changing endpoints (POST, PUT, DELETE, PATCH) that rely on ambient credentials (cookies, basic auth) without CSRF tokens or SameSite cookie protection allow malicious third-party websites to execute actions on behalf of authenticated users.

## Applies To
- Traditional Form Submissions, Cookie-Authenticated REST APIs
- Express (csurf), Django, Flask (Flask-WTF), Rails, Spring Security, ASP.NET Core

## Why It Matters
If a banking or SaaS application authenticates requests solely via browser cookies, a user visiting a malicious site can be tricked into submitting unauthorized form requests that the browser will automatically authenticate with the user's cookies.

## What TorusGuard Looks For
- State-changing route handlers lacking CSRF middleware, CSRF tokens in headers, or explicit SameSite cookie configurations.
- Explicit disabling of CSRF protection (e.g. `@csrf_exempt`, `csrf().disable()`).

## Unsafe Example
```python
# UNSAFE: Disabling CSRF protection on state-changing endpoint
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_email(request):
    request.user.email = request.POST.get("email")
    request.user.save()
```

## Safe Example
```python
# SAFE: Enforcing CSRF token verification
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def update_email(request):
    request.user.email = request.POST.get("email")
    request.user.save()
```

## Ponytail Remediation Budget
- Additions: <= 4 lines
- Deletions: <= 2 lines

## Remediation
1. Never disable framework CSRF protection with `@csrf_exempt` or `csrf().disable()`.
2. Configure session cookies with `SameSite: 'Lax'` or `'Strict'`.
3. For single-page applications, validate custom headers (e.g. `X-Requested-With`, `X-CSRF-Token`).

## Related Rules
- `TG-AUTH-004`: Insecure Session Cookie Configuration
- `TG-PLATFORM-001`: Wildcard CORS With Credentials
