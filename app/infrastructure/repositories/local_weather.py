from typing import List, Optional, Tuple

import bson
import logging

from motor.motor_asyncio import AsyncIOMotorCursor

from app.domain.models import LocalWeatherModel
from app.domain.interfaces import RepositoryInterface
from app.infrastructure.db import DatabaseConnectionHandler, PyObjectId
from app.infrastructure.schemas import (
    LocalWeatherBaseSchema,
    PaginationParams,
    LocalWeatherCreateSchema,
    LocalWeatherUpdateSchema,
)
from app.application.errors import NotFoundError


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LocalWeatherRepository(RepositoryInterface[LocalWeatherBaseSchema]):
    def __init__(self, db_handler: DatabaseConnectionHandler):
        if db_handler.collection is None:
            raise ValueError("db_handler.collection is None")
        self.collection = db_handler.collection

    @staticmethod
    def _get_object_id(id: str) -> bson.ObjectId:
        return bson.ObjectId(id)

    @staticmethod
    def _convert_id_to_str(data: dict) -> dict:
        data["id"] = str(data["_id"])
        return data

    async def create(
        self, data: LocalWeatherCreateSchema
    ) -> Optional[LocalWeatherBaseSchema]:
        local_weather_data = data.dict()
        local_weather_data["id"] = PyObjectId()
        weather_model = LocalWeatherModel(**local_weather_data)
        await self.collection.insert_one(weather_model.dict(by_alias=True))

        weather_dict = weather_model.dict()
        weather_dict["id"] = str(weather_dict["id"])
        return LocalWeatherBaseSchema.parse_obj(weather_dict)

    async def find_by_id(self, id: str) -> Optional[LocalWeatherBaseSchema]:
        oid = self._get_object_id(id)
        local_weather = await self.collection.find_one({"_id": oid})
        if local_weather is None:
            raise NotFoundError
        return LocalWeatherBaseSchema.parse_obj(self._convert_id_to_str(local_weather))

    async def find_most_recent_by_name(
        self, name: str
    ) -> Optional[LocalWeatherBaseSchema]:
        local_weather = await self.collection.find_one(
            {"name": name}, sort=[("created_at", -1)]
        )
        if local_weather:
            return LocalWeatherBaseSchema.parse_obj(
                self._convert_id_to_str(local_weather)
            )
        else:
            return None

    async def find_all(
        self, pagination: PaginationParams
    ) -> Tuple[List[LocalWeatherBaseSchema], int, int]:
        local_weathers_cursor: AsyncIOMotorCursor = self.collection.find()
        total = await self.collection.count_documents({})
        local_weathers = await local_weathers_cursor.skip(pagination.skip).to_list(
            length=pagination.limit
        )
        total_with_pagination = len(local_weathers)
        if local_weathers:
            return (
                [
                    LocalWeatherBaseSchema.parse_obj(
                        self._convert_id_to_str(local_weather)
                    )
                    for local_weather in local_weathers
                ],
                total,
                total_with_pagination,
            )
        return [], total, total_with_pagination

    async def update(
        self, id: str, data: LocalWeatherUpdateSchema
    ) -> Optional[LocalWeatherBaseSchema]:
        oid = self._get_object_id(id)
        result = await self.collection.update_one(
            {"_id": oid}, {"$set": data.dict(exclude_unset=True)}
        )
        if result.modified_count == 0:
            raise NotFoundError
        return await self.find_by_id(id)

    async def delete_by_id(self, id: str) -> bool:
        oid = self._get_object_id(id)
        result = await self.collection.delete_one({"_id": oid})
        return result.deleted_count > 0
