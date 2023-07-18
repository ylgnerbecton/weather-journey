import pytest
from app.infrastructure.db import PyObjectId
from fastapi import status


class TestLocalWeatherView:
    @pytest.fixture(autouse=True)
    async def setup_and_teardown(self, mongo_db_session):
        self.test_local_weather_name = "Lisboa"
        self.collection = mongo_db_session["local_weather"]
        yield
        await self.collection.delete_many({"name": self.test_local_weather_name})

    @pytest.mark.asyncio
    async def test_post_local_weather(self, test_client):
        response = await test_client.post(
            "/local-weather", json={"name": self.test_local_weather_name}
        )
        assert response.status_code == status.HTTP_201_CREATED
        response_body = response.json()

        assert "response_data" in response_body
        response_data = response_body["response_data"]
        assert "name" in response_data
        assert response_data["name"] == self.test_local_weather_name
        assert "description" in response_data
        assert "specs" in response_data
        assert "created_at" in response_data
        assert "updated_at" in response_data

        inserted_document = await self.collection.find_one(
            {"name": self.test_local_weather_name}
        )
        assert inserted_document is not None
        assert inserted_document["name"] == self.test_local_weather_name
        assert PyObjectId.is_valid(inserted_document["_id"])

    @pytest.mark.asyncio
    async def test_post_local_weather_error_handling(self, test_client):
        response = await test_client.post("/local-weather", json={"name": 123})
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
