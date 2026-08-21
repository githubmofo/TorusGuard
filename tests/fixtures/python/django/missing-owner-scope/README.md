# Regression Fixture: Missing Owner Scope (IDOR)

- **Framework:** Django
- **Target Rule:** `TG-AUTH-007`
- **Expected Classification:** `Confirmed`
- **Expected Rule IDs:** `TG-AUTH-007`
- **Reasoning:** Lookups directly performing `Document.objects.get(id=doc_id)` without filtering by `owner=request.user` allow any authenticated user to read documents belonging to other users.

## Sample Code
```python
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import Document

@login_required
def view_document(request, doc_id):
    # VULNERABLE: Lacks owner scoping
    doc = Document.objects.get(id=doc_id)
    return JsonResponse({"id": doc.id, "title": doc.title})
```
