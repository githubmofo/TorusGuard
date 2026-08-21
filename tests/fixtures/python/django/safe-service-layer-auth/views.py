from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required

class InvoiceService:
    @staticmethod
    def get_invoice_for_user(invoice_id, user):
        # Simulated domain service enforcing ownership
        if user.is_authenticated and invoice_id > 0:
            return {"id": invoice_id, "amount": 100.0, "owner_id": user.id}
        return None

@login_required
def view_invoice(request, invoice_id):
    invoice = InvoiceService.get_invoice_for_user(invoice_id, user=request.user)
    if not invoice:
        raise Http404("Invoice not found or access denied.")
    return JsonResponse(invoice)
