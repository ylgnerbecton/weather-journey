from typing import Type, TypeVar
from http import HTTPStatus
from fastapi import APIRouter, HTTPException, status

from app.infrastructure.schemas import (
    LocalWeatherBaseSchema,
    LocalWeatherCreateSchema,
    LocalWeatherUpdateSchema,
    ResponseObjectSchema,
)
from app.domain.services import LocalWeatherService
from .base import BaseView


class LocalWeatherView(BaseView):
    resource_name = "local-weather"
    service_layer = LocalWeatherService()
    create_schema = LocalWeatherCreateSchema
    update_schema = LocalWeatherUpdateSchema
    get_schema = LocalWeatherBaseSchema

    # example:
    # @classmethod
    # async def _create_item(cls, request: create_model):
    #     try:
    #         item = await cls.service_layer.create(data=request)
    #         return item
    #     except Exception as e:
    #         raise HTTPException(
    #             detail=str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR
    #         )

    # @classmethod
    # def setup(cls):
    #     super().setup()
    #     @cls.router.post(
    #         f"/{cls.resource_name}/example",
    #         status_code=status.HTTP_201_CREATED,
    #         response_model=ResponseObjectSchema[cls.create_model],
    #     )
    #     async def create_item_example(request: cls.create_model):
    #         try:
    #             return await cls.service_layer.create(data=request)
    #         except Exception as e:
    #             raise HTTPException(
    #                 detail=str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR
    #             )


LocalWeatherView.setup()
