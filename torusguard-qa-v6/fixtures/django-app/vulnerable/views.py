from django.shortcuts import render
from django.utils.safestring import mark_safe
from .models import Invoice

def invoice_detail(request, invoice_id):
    # IDOR Vulnerability: Missing tenant filter
    invoice = Invoice.objects.get(id=invoice_id)
    # Template autoescaping bypass
    rendered = mark_safe(f"<h1>{invoice.title}</h1>")
    return render(request, "detail.html", {"content": rendered})
