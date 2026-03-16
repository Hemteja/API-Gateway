from pydantic import BaseModel, HttpUrl
from datetime import datetime

class RouteCreate(BaseModel):
    name: str
    target_url: str
    rate_limit: int = 100
    rate_limit_window: int = 60

class RouteResponse(BaseModel):
    id: int
    name: str
    target_url: str
    rate_limit: int
    rate_limit_window: int
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True
