import os

os.environ["DB_USER"] = "test_user"
os.environ["DB_PASSWORD"] = "test_password"
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "5432"
os.environ["DB_NAME"] = "test_db"

os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6379"

from typing import AsyncGenerator

import pytest
from fakeredis.aioredis import FakeRedis
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.api.__main__ import app
from src.api.database.connection import get_db
from src.api.repositories.calculator import CalculatorRepository


@pytest.mark.asyncio
async def test_api(
    sessionmaker: async_sessionmaker[AsyncSession],
    mocker: MockerFixture,
    redis: FakeRedis,
) -> None:
    mocker.patch("src.api.services.cache.r", redis)

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with sessionmaker() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with sessionmaker() as session:
        repo = CalculatorRepository(session)

        await repo.teach("2+2", "4")
        await repo.teach("2+2", "5")
        await repo.teach("2+2", "4")
        await session.commit()

    try:
        client = TestClient(app)

        response = client.get("/calculate", params={"expr": "2+2"})
        assert response.status_code == 200
        data = response.json()
        assert data["expression"] == "2+2"
        assert data["result"] == "4"
        assert data["total_votes"] == 3
    finally:
        app.dependency_overrides.pop(get_db, None)
