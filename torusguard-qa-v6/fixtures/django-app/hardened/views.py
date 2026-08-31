from django.shortcuts import render, get_object_or_404
from .models import Invoice

def invoice_detail(request, invoice_id):
    # Hardened: Tenant scoped query
    invoice = get_object_or_404(Invoice, id=invoice_id, tenant_id=request.user.tenant_id)
    # Autoescaped in Django template
    return render(request, "detail.html", {"invoice": invoice})
