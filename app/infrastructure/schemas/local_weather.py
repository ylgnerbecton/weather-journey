from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class LocalWeatherBaseSchema(BaseModel):
    id: Optional[str] = Field(
        None, description="The unique identifier of the local weather"
    )
    name: str = Field(..., description="Name of the local weather")
    description: Optional[str] = Field(
        None, description="Description of the local weather"
    )
    specs: Optional[Dict[str, Any]] = Field(
        None, description="Additional specifications related to the local weather"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True

    def dict(self, *args, **kwargs):
        obj = super().dict(*args, **kwargs)
        obj["name"] = obj["name"].title()
        return obj


class LocalWeatherCreateSchema(LocalWeatherBaseSchema):
    pass


class LocalWeatherUpdateSchema(LocalWeatherBaseSchema):
    pass
