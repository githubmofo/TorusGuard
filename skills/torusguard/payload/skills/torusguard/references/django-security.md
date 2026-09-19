# TorusGuard Skill Reference: Django Security

> **Loaded When:** A project is identified as a Django application (`manage.py`, `settings.py`, or `django` dependency detected).

---

## 🛡️ Key Inspection Areas & Rules

### 1. Secrets & Production Configuration
* `TG-SEC-001`: Verify `SECRET_KEY` is loaded via `os.environ` or a secrets manager, not hardcoded.
* `TG-PLATFORM-003`: Verify `DEBUG = False` in production configs.
* `TG-PLATFORM-001`: Ensure `ALLOWED_HOSTS` is restricted to legitimate hostnames.

### 2. Authentication & Authorization
* `TG-AUTH-001`: Ensure protected views use `@login_required` or `LoginRequiredMixin`.
* `TG-AUTH-007`: Enforce object-level ownership checks (e.g. `get_object_or_404(Model, id=id, user=request.user)`). Avoid unrestricted numeric ID lookups.

### 3. Mass Assignment
* `TG-AUTH-006`: Ensure `ModelForm` definitions specify explicit `fields = [...]` lists instead of `fields = '__all__'`.

### 4. Injection & Database Security
* `TG-INPUT-003`: Ensure `Model.objects.raw()` or `cursor.execute()` uses parameterized inputs (`%s`), never f-strings or `.format()`.

### 5. CSRF & Request Security
* `TG-CSRF-001`: Verify `django.middleware.csrf.CsrfViewMiddleware` is active in `MIDDLEWARE`. Avoid indiscriminate `@csrf_exempt`.
* `TG-CACHE-001`: Verify sensitive authenticated endpoints use `@never_cache`.

---

## 🛠️ Safe Patterns Summary
```python
# Safe Object Lookup
item = get_object_or_404(Invoice, id=invoice_id, account=request.user.account)

# Safe Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'website_url', 'avatar']

# Safe Raw SQL (if mandatory)
cursor.execute("SELECT * FROM reports WHERE account_id = %s", [request.user.account_id])
```
