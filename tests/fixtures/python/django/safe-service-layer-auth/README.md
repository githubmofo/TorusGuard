# Regression Fixture: Safe Service-Layer Authorization

- **Framework:** Django
- **Target Rule:** `TG-AUTH-007`
- **Expected Classification:** `Manual Review` / Safe
- **Expected Rule IDs:** `TG-AUTH-007` (Verified safe in domain service layer)
- **Reasoning:** In domain-driven architectures, views may delegate queryset filtering to a backend service layer (`InvoiceService.get_invoice_for_user(invoice_id, request.user)`). TorusGuard must not label this pattern as a confirmed vulnerability without inspecting the service implementation.

## Sample Code
```python
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from .services import InvoiceService

@login_required
def view_invoice(request, invoice_id):
    # Service layer explicitly enforces user ownership check
    invoice = InvoiceService.get_invoice_for_user(invoice_id, user=request.user)
    if not invoice:
        raise Http404("Invoice not found or access denied.")
    return JsonResponse({"id": invoice.id, "amount": invoice.amount})
```
