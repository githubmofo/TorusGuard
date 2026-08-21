# DRF Security Research Notes (TorusGuard v0.4.0)

## Research Findings
- **Permissions vs Throttling:** Permissions control access decisions; throttling mitigates temporary high-frequency abuse but does not replace authentication or anti-automation layers.
- **Queryset Scoping:** In DRF `ModelViewSet` instances, overriding `get_queryset()` is the primary server-side barrier against multi-tenant IDOR.
- **Serializer Protection:** ModelSerializers without explicit `read_only_fields` allow attackers to manipulate permission-granting flags (`is_staff`, `role`).
