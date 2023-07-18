from typing import TypeVar, Generic, List, Optional, Tuple
from abc import ABC, abstractmethod
from pydantic import BaseModel

from app.infrastructure.schemas import Response, PaginationParams


T = TypeVar("T", bound=BaseModel)


class RepositoryInterface(Generic[T], ABC):
    @abstractmethod
    async def create(self, data: T) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, id: str) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, pagination: PaginationParams) -> Tuple[List[T], int, int]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: str, data: T) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, id: str) -> bool:
        raise NotImplementedError


class ServiceInterface(Generic[T], ABC):
    @abstractmethod
    async def create(self, data: T) -> Optional[Response]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: str) -> Optional[Response]:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, pagination: PaginationParams) -> Optional[Response]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: str, data: T) -> Optional[Response]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: str) -> Response:
        raise NotImplementedError
