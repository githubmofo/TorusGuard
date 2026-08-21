# Regression Fixture: Safe DRF Read-Only Fields

- **Framework:** Django REST Framework (DRF)
- **Target Rule:** `TG-AUTH-006`
- **Expected Classification:** Safe (No findings)
- **Expected Rule IDs:** None / Safe
- **Reasoning:** Serializer declares `read_only_fields` for all privilege and system-controlled fields (`is_staff`, `role`, `tier`). TorusGuard should recognize this as safe.

## Sample Code
```python
from rest_framework import serializers

class UserAccountSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    role = serializers.CharField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
```
