# Remediation Mapping: Django Vulnerable -> Hardened

| Vulnerability / Risk | Rule ID | Vulnerable File | Hardened File | Security Control Applied |
|---|---|---|---|---|
| Hardcoded Development Secret | `TG-SEC-001` | `config/settings.py` | `config/settings.py` | Load secret from `os.environ.get("DJANGO_SECRET_KEY")` |
| DEBUG enabled in production | `TG-PLATFORM-003` | `config/settings.py` | `config/settings.py` | Set `DEBUG = False` and enforce explicit `ALLOWED_HOSTS` |
| Document View IDOR | `TG-AUTH-007` | `accounts/views.py` | `accounts/views.py` | Add ownership filtering (`Document.objects.filter(owner=request.user)`) |
| Profile Form Mass Assignment | `TG-AUTH-006` | `accounts/forms.py` | `accounts/forms.py` | Replace `fields = '__all__'` with explicit safe whitelist |
| Sensitive Profile Caching | `TG-CACHE-001` | `accounts/views.py` | `accounts/views.py` | Apply `@never_cache` decorator |
