from typing import Any, Dict

from app.infrastructure.db import BaseModel


class LocalWeatherModel(BaseModel):
    name: str
    description: str
    specs: Dict[str, Any]

    class Config(BaseModel.Config):
        schema_extra = {"collection": "local_weather"}
