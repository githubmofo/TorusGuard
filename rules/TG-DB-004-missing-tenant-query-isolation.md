---
id: TG-DB-004
title: Missing Tenant Query Isolation in Multi-Tenant Models
category: data-access-orm
severity: Critical
confidence: Confirmed
frameworks:
  - django
  - drf
  - fastapi
  - flask
  - sqlalchemy
cwe: CWE-284
asvs_v4: V4.1.3
nist_ssdf: PW.5.1
---

# TG-DB-004: Missing Tenant Query Isolation in Multi-Tenant Models

## 🚨 Problem Statement
In multi-tenant web applications, querying database tables by primary key (`id` or `uuid`) without explicitly binding or filtering by the authenticated user's `tenant_id` (or organization ID) permits horizontal cross-tenant data exfiltration (IDOR across organization boundaries).

---

## 💥 Adversarial Threat & Exploitation
An attacker from Tenant B supplies the record UUID of a confidential document belonging to Tenant A:
```http
GET /api/v1/invoices/9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d HTTP/1.1
Host: saas.example.com
Authorization: Bearer <Tenant_B_JWT>
```
If the backend performs `session.get(Invoice, invoice_id)` or `Invoice.objects.get(id=invoice_id)` without scoping to `tenant_id=current_user.tenant_id`, the invoice belonging to Tenant A is returned to the attacker.

---

## 🛠️ Framework-Native Remediations

### 🐍 SQLAlchemy (Scoped Tenant Queries)

#### ❌ Unsafe Pattern
```python
# Unsafe: Global primary key lookup without tenant filter
@app.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice
```

#### ✅ Safe Remediation
```python
# Safe: Enforce tenant scoping on every query filter
@app.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    invoice = (
        db.query(Invoice)
        .filter(Invoice.id == invoice_id, Invoice.tenant_id == user.tenant_id)
        .first()
    )
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice
```

---

### 🐍 Django ORM (Scoped Manager / ViewSet Queryset)

#### ❌ Unsafe Pattern
```python
# Unsafe: Global queryset in DRF ViewSet
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()  # Exposes all tenant records
    serializer_class = InvoiceSerializer
```

#### ✅ Safe Remediation
```python
# Safe: Override get_queryset to enforce tenant boundary on every request
class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Strictly scope lookups to authenticated user's organization
        return Invoice.objects.filter(tenant=self.request.user.tenant)
```

---

## 🧪 Verification & Reproduction
1. Send request with valid Tenant B token requesting Tenant A resource ID:
   ```bash
   curl -H "Authorization: Bearer <Tenant_B_Token>" http://localhost:8000/invoices/<Tenant_A_UUID>
   ```
2. **Assertion:** Request must return `404 Not Found`, denying access to cross-tenant data.
