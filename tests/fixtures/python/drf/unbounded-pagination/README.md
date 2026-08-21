# Regression Fixture: Unbounded Pagination in DRF

- **Framework:** Django REST Framework (DRF)
- **Target Rule:** `TG-RATE-002`
- **Expected Classification:** `Confirmed`
- **Expected Rule IDs:** `TG-RATE-002`
- **Reasoning:** `PageNumberPagination` specifying `page_size_query_param` without setting `max_page_size` allows clients to request `?page_size=10000000`, exhausting database and worker memory.

## Sample Code
```python
from rest_framework.pagination import PageNumberPagination

class UnsafePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'  # ❌ Missing max_page_size ceiling
```
