# TG-AUTH-007: Missing Object-Level and Property-Level Authorization (IDOR)

## Severity
High by default. Raise to Critical when financial, healthcare, or administrative records are exposed without tenant boundaries.

## Applies To
- Database query handlers, REST API endpoints, GraphQL resolvers, RPC methods, and service layers across Node.js, Express, Django, DRF, FastAPI, Flask, and SQLAlchemy.

## Why It Matters
When an application retrieves, modifies, or deletes an object using a client-supplied identifier (`id`, `order_id`, `invoice_id`) without verifying that the requesting user owns or has legitimate access to that specific object, attackers can perform Insecure Direct Object References (IDOR) to access records belonging to other tenants.

## What TorusGuard Looks For
- Query lookups using solely URL parameters or payload primary keys (e.g. `Model.objects.get(id=pk)`, `session.query(Order).filter(Order.id == order_id)`) without tenant/user ownership criteria.
- Serializers and API endpoints that expose or mutate private sub-resources without validating the parent-child tenant relationship.

## Evidence & Classification Standards
- **`Confirmed`:** The query or view directly executes database lookups using an unsanitized client identifier with zero user/tenant filter criteria in the same module.
- **`Manual Review`:** The view delegates fetching to a separate domain or service layer (e.g. `InvoiceService.get_invoice(id, request.user)`). The reviewer must inspect the service layer to confirm tenant enforcement.
- **`Informational`:** Read-only queries against intentionally public or catalog records.

## Unsafe Examples

### Python (Django / DRF)
```python
# VULNERABLE: Direct lookup without owner filter
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()  # ❌ Exposes all invoices to any user
    serializer_class = InvoiceSerializer
```

### Python (SQLAlchemy)
```python
# VULNERABLE: Direct primary key filter
def get_order(session, order_id: int):
    return session.query(Order).filter(Order.id == order_id).first()  # ❌ Missing user_id
```

## Safe Examples

### Python (Django / DRF)
```python
# SAFE: Scope queryset to authenticated user
class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(owner=self.request.user)  # ✅ Scoped
```

### Python (SQLAlchemy)
```python
# SAFE: Scoped query
def get_order(session, order_id: int, current_user_id: int):
    return session.query(Order).filter(
        Order.id == order_id, 
        Order.user_id == current_user_id
    ).first()  # ✅ Scoped to user
```

## Remediation
1. Ensure all object lookups include the current user/tenant ID in the database query (`filter(user_id=request.user.id)`).
2. For DRF ViewSets, override `get_queryset()` to filter by `self.request.user`.
3. In service-layer architectures, pass the authenticated user identity explicitly into domain methods.

## Verification
- Run authenticated test requests using User A's credentials against User B's resource IDs and assert `404 Not Found` or `403 Forbidden`.

## Related Rules
- `TG-AUTH-006`: Mass Assignment
- `TG-AUTH-001`: Unauthenticated Endpoints
