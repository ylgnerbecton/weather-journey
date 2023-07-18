from datetime import datetime, timedelta
from typing import Optional
from app.domain.interfaces import ServiceInterface
from app.infrastructure.repositories import LocalWeatherRepository
from app.infrastructure.schemas import (
    Response,
    LocalWeatherBaseSchema,
    PaginationParams,
    ResponseListSchema,
    LocalWeatherCreateSchema,
    LocalWeatherUpdateSchema,
)
from app.config import Settings
from app.infrastructure.db import DatabaseConnectionHandler
from app.application.adapters import OpenWeatherMapAPI

settings = Settings()


class LocalWeatherService(ServiceInterface[LocalWeatherBaseSchema]):
    def __init__(self) -> None:
        db_handler = DatabaseConnectionHandler(collection_name="local_weather")
        if db_handler.collection is None:
            raise ValueError("db_handler.collection is None")
        self.repository = LocalWeatherRepository(db_handler)
        self.weather_api = OpenWeatherMapAPI()

    async def create(self, data: LocalWeatherCreateSchema) -> Response:
        normalized_name = data.name.lower()
        recent_weather = await self.repository.find_most_recent_by_name(normalized_name)
        if recent_weather and (
            datetime.utcnow() - recent_weather.created_at < timedelta(days=1)
        ):
            return Response.build(recent_weather)

        description, specs = self.weather_api.get_forecast_and_data(data.name)
        if description is None or specs is None:
            raise ValueError(f"Could not get weather for city: {data.name}")

        local_weather_data = LocalWeatherCreateSchema(
            name=normalized_name, description=description, specs=specs
        )

        local_weather = await self.repository.create(local_weather_data)
        return Response.build(local_weather)

    async def get(self, id: str) -> Response:
        local_weather = await self.repository.find_by_id(id)
        return Response.build(local_weather)

    async def get_all(self, pagination: PaginationParams) -> ResponseListSchema:
        local_weathers, total, total_with_pagination = await self.repository.find_all(
            pagination
        )
        return ResponseListSchema.build_with_pagination(
            local_weathers, pagination, total, total_with_pagination
        )

    async def update(self, id: str, data: LocalWeatherUpdateSchema) -> Response:
        local_weather = await self.repository.update(id, data)
        return Response.build(local_weather)

    async def delete(self, id: str) -> Response:
        local_weather = await self.repository.find_by_id(id)
        await self.repository.delete_by_id(id)
        return Response.build(local_weather)
