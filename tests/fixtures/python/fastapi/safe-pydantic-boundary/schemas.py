class ConfigDict:
    def __init__(self, extra="forbid"):
        self.extra = extra

class BaseModel:
    pass

class ProfileUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    bio: str
    display_name: str
