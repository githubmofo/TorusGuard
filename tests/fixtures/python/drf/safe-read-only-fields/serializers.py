class BaseSerializer:
    pass

class UserAccountSerializer(BaseSerializer):
    # Simulated DRF Serializer with explicit read-only fields
    fields = ['id', 'username', 'email', 'role', 'is_staff']
    read_only_fields = ['id', 'role', 'is_staff']
