from typing import Type, TypeVar
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

from app.application.errors import NotFoundError
from app.infrastructure.schemas import (
    ResponseListSchema,
    ResponseObjectSchema,
    PaginationParams,
)

T = TypeVar("T", bound=BaseModel)


class BaseView:
    resource_name: str
    service_layer: Type[T]
    create_schema: Type[T]
    update_schema: Type[T]
    get_schema: Type[T]

    router = APIRouter()

    @classmethod
    def setup(cls):
        cls.router.tags = [cls.resource_name]

        @cls.router.post(
            f"/{cls.resource_name}",
            status_code=status.HTTP_201_CREATED,
            response_model=ResponseObjectSchema[cls.create_schema],
        )
        async def create_item(request: cls.create_schema):
            return await cls._create_item(request)

        @cls.router.get(
            f"/{cls.resource_name}",
            status_code=status.HTTP_200_OK,
            response_model=ResponseListSchema[cls.get_schema],
        )
        async def get_items(pagination: PaginationParams = Depends()):
            return await cls._get_items(pagination)

        @cls.router.get(
            f"/{cls.resource_name}/{{id}}",
            status_code=status.HTTP_200_OK,
            response_model=ResponseObjectSchema[cls.get_schema],
        )
        async def get_item_by_id(id: str):
            return await cls._get_item_by_id(id)

        @cls.router.put(
            f"/{cls.resource_name}/{{id}}",
            status_code=status.HTTP_200_OK,
            response_model=ResponseObjectSchema[cls.update_schema],
        )
        async def update_item(id: str, request: cls.update_schema):
            return await cls._update_item(id, request)

        @cls.router.delete(
            f"/{cls.resource_name}/{{id}}",
            status_code=status.HTTP_200_OK,
            response_model=ResponseObjectSchema[cls.get_schema],
        )
        async def delete_item(id: str):
            return await cls._delete_item(id)

    @classmethod
    async def _create_item(cls, request):
        try:
            return await cls.service_layer.create(data=request)
        except Exception as e:
            raise HTTPException(
                detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @classmethod
    async def _get_items(cls, pagination: PaginationParams):
        try:
            return await cls.service_layer.get_all(pagination)
        except Exception as e:
            raise HTTPException(
                detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @classmethod
    async def _get_item_by_id(cls, id: str):
        try:
            return await cls.service_layer.get(id=id)
        except NotFoundError as e:
            raise HTTPException(detail=e.description, status_code=e.code)
        except Exception as e:
            raise HTTPException(
                detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @classmethod
    async def _update_item(cls, id: str, request):
        try:
            return await cls.service_layer.update(id=id, data=request)
        except NotFoundError as e:
            raise HTTPException(detail=e.description, status_code=e.code)
        except Exception as e:
            raise HTTPException(
                detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @classmethod
    async def _delete_item(cls, id: str):
        try:
            return await cls.service_layer.delete(id=id)
        except NotFoundError as e:
            raise HTTPException(detail=e.description, status_code=e.code)
        except Exception as e:
            raise HTTPException(
                detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
