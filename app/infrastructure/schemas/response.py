from datetime import datetime
from typing import TypeVar, Generic, Type, List, Optional
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")


class Response(GenericModel, Generic[DataT]):
    server_unix_timestamp: int = Field(
        default_factory=lambda: int(datetime.now().timestamp()),
        description="Server's Unix timestamp at the moment of the response",
    )
    response_data: DataT = Field(..., description="The response data")

    @classmethod
    def build(cls: Type["Response[DataT]"], response: DataT):
        return cls(response_data=response)


class ResponseObjectSchema(Response[DataT], Generic[DataT]):
    pass


class PaginationParams(BaseModel):
    skip: int = Field(0, description="Number of entries to skip for pagination")
    limit: int = Field(100, description="Maximum number of entries to return")


class ResponseListSchema(Response[List[DataT]], Generic[DataT]):
    skip: Optional[int] = Field(
        None, description="Number of entries to skip for pagination"
    )
    limit: Optional[int] = Field(
        None, description="Maximum number of entries to return"
    )
    total: Optional[int] = Field(None, description="Total number of entries")
    total_with_pagination: Optional[int] = Field(
        None, description="Maximum number of entries to return"
    )

    @classmethod
    def build_with_pagination(
        cls: Type["ResponseListSchema[DataT]"],
        response: DataT,
        pagination: PaginationParams,
        total,
        total_with_pagination,
    ):
        return cls(
            response_data=response,
            skip=pagination.skip,
            limit=pagination.limit,
            total=total,
            total_with_pagination=total_with_pagination,
        )
