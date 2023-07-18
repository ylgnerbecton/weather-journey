import pytest
import httpx
import asyncio

from motor import motor_asyncio
from fastapi import FastAPI
from app.presentation.views import health_check_router
from app.presentation.views import LocalWeatherView
from app.config import Settings


@pytest.fixture(scope="module", name="settings")
def settings() -> Settings:
    return Settings(
        DATABASE_URL="mongodb://db_weather:27017",
        DB_NAME="local",
    )


@pytest.fixture
async def mongo_db_session(settings):
    client = motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URL)
    db = client[settings.DB_NAME]
    yield db
    client.close()


@pytest.fixture
def assert_all_responses_were_requested() -> bool:
    return False


@pytest.fixture(scope="module")
def test_app(settings):
    app = FastAPI(root_path=settings.API_ROOT_PATH)
    app.include_router(health_check_router)
    app.include_router(LocalWeatherView.router)
    return app


@pytest.fixture
async def test_client(test_app):
    await asyncio.sleep(1)
    async with httpx.AsyncClient(app=test_app, base_url="http://localhost:8010") as client:
        yield client
