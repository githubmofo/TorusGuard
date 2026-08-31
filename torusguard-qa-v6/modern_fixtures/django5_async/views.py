import os
from django.http import JsonResponse
from asgiref.sync import sync_to_async
from .models import Invoice

async def get_invoice_async(request, invoice_id: int):
    # Async IDOR Vulnerability in Django 5.x
    invoice = await Invoice.objects.aget(id=invoice_id)
    return JsonResponse({"id": invoice.id, "title": invoice.title})
