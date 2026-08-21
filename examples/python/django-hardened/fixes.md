# Hardened Fixes Matrix: Django

| Risk | Rule ID | Hardened Implementation |
|---|---|---|
| Hardcoded Secret | `TG-SEC-001` | `SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")` with validation guard |
| Production Debug Mode | `TG-PLATFORM-003` | `DEBUG = False`, `ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")` |
| IDOR in Document Access | `TG-AUTH-007` | `doc = get_object_or_404(Document, id=doc_id, owner=request.user)` |
| Mass Assignment in Form | `TG-AUTH-006` | `fields = ['first_name', 'last_name', 'email', 'bio']` |
| Sensitive Profile Cache | `TG-CACHE-001` | `@never_cache` decorator applied on `profile_view` |
