# TG-AUTH-006: Mass Assignment & Privilege Escalation via Payloads

## Severity
High by default. Raise to Critical when client payloads can alter administrative roles (`is_staff`, `is_superuser`, `role`), account status, or billing tiers.

## Applies To
- Form handlers, model binders, ORM update operations, DRF serializers, and FastAPI/Pydantic ingestion schemas.

## Why It Matters
When server code automatically binds arbitrary client JSON/form keys to internal database models without field-level allowlists, clients can inject sensitive attributes (e.g. `{"role": "admin", "is_verified": true}`) to elevate their privileges.

## What TorusGuard Looks For
- Django `ModelForm` classes declaring `fields = '__all__'`.
- DRF serializers without `read_only_fields` on privilege or system columns.
- FastAPI/Pydantic schemas omitting `extra="forbid"` or binding directly to ORM models.
- SQLAlchemy `.update(request_data)` executing raw untrusted dictionaries.

## Evidence & Classification Standards
- **`Confirmed`:** `fields = '__all__'` in Django ModelForms or raw `.update(payload)` without allowlists on models containing privilege fields.
- **`Safe`:** Serializers using explicit `read_only_fields = ['role', 'is_staff']` or Pydantic models using `ConfigDict(extra="forbid")`.

## Unsafe Examples

### Django ModelForm
```python
# VULNERABLE: Binds all model fields to form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'  # ❌ Allows user to submit is_staff=True
```

### DRF Serializer
```python
# VULNERABLE: Missing read_only_fields
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_staff']  # ❌ role & is_staff are writable
```

## Safe Examples

### Django ModelForm
```python
# SAFE: Explicit editable fields whitelist
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['display_name', 'bio', 'avatar_url']  # ✅ Only safe fields exposed
```

### DRF Serializer
```python
# SAFE: Explicit read_only_fields
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_staff']
        read_only_fields = ['id', 'role', 'is_staff']  # ✅ System fields protected
```

## Remediation
1. Use explicit field allowlists rather than wildcard binds.
2. In DRF serializers, declare `read_only_fields` for all privilege, status, and financial properties.
3. In Pydantic v2 schemas, configure `model_config = ConfigDict(extra="forbid")`.

## Related Rules
- `TG-AUTH-007`: Missing Property-Level Authorization
- `TG-INPUT-001`: Unvalidated Client Input
