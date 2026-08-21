# Regression Fixture: Safe Pydantic Schema Boundary

- **Framework:** FastAPI / Pydantic v2
- **Target Rule:** `TG-AUTH-006`
- **Expected Classification:** Safe (No findings)
- **Expected Rule IDs:** None / Safe
- **Reasoning:** Ingestion schema explicitly specifies `extra = "forbid"` and explicit fields, preventing mass-assignment attribute injection.

## Sample Code
```python
from pydantic import BaseModel, ConfigDict, Field

class ProfileUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    bio: str = Field(max_length=500)
    display_name: str = Field(max_length=100)
```
