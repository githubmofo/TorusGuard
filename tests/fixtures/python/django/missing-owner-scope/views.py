from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required

class MockDocumentManager:
    @staticmethod
    def get(id):
        return {"id": id, "title": "Confidential Report", "owner_id": 999}

@login_required
def view_document(request, doc_id):
    # VULNERABLE: Direct ID lookup without owner filter
    doc = MockDocumentManager.get(id=doc_id)
    return JsonResponse(doc)
