import os

os.environ["DB_USER"] = "test_user"
os.environ["DB_PASSWORD"] = "test_password"
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "5432"
os.environ["DB_NAME"] = "test_db"

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.api.repositories.calculator import CalculatorRepository


@pytest.mark.asyncio
async def test_calculator_repository(
    sessionmaker: async_sessionmaker[AsyncSession],
) -> None:
    async with sessionmaker() as session:
        repo = CalculatorRepository(session)

        await repo.teach("2+2", "4")
        result = await repo.calculate("2+2")
        assert result is not None
        assert result["expression"] == "2+2"
        assert result["result"] == "4"
        assert result["total_votes"] == 1

        await repo.teach("2+2", "5")
        result = await repo.calculate("2+2")
        assert result is not None
        assert result["expression"] == "2+2"
        assert result["result"] == "4"
        assert result["total_votes"] == 2

        await repo.teach("2+2", "4")
        result = await repo.calculate("2+2")
        assert result is not None
        assert result["expression"] == "2+2"
        assert result["result"] == "4"
        assert result["total_votes"] == 3
