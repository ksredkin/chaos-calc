import os

import uvicorn
from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.connection import get_db
from src.api.repositories.calculator import CalculatorRepository
from src.api.schemas.calculation import CalculationCreate
from src.api.services.cache import cache
from src.api.utils.logger import Logger

logger = Logger("API")

app = FastAPI(
    prefix="/api/v1",
    title="Chaos Calculator API",
    description="API для обучения и получения результатов математических выражений",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/calculate",
    response_model=dict[str, str | int],
    description="Получить результат математического выражения. Если результат неизвестен, возвращает сообщение об этом.",
)
async def calculate(
    expr: str = Query(
        ...,
        min_length=1,
        max_length=50,
        pattern=r"^[0-9+\-*/().]+$",
        description="Математическое выражение",
    ),
    session: AsyncSession = Depends(get_db),
) -> dict[str, str | int]:
    cached_result = await cache.get_expression_result(expr)
    if cached_result:
        return cached_result

    repository = CalculatorRepository(session)
    result = await repository.calculate(expr)
    return (
        result
        if result
        else {"expression": expr, "result": "Я не знаю сколько это", "total_votes": 0}
    )


@app.post(
    "/teach",
    response_model=dict[str, str | int],
    description="Научить калькулятор результату математического выражения. Если выражение уже известно, увеличивает счетчик голосов за этот результат.",
)
async def teach(
    calculation: CalculationCreate, session: AsyncSession = Depends(get_db)
) -> dict[str, str | int]:
    repository = CalculatorRepository(session)
    await repository.teach(calculation.expression, calculation.result)
    leader = await repository.calculate(calculation.expression)
    if leader:
        await cache.set_expression_result(calculation.expression, leader)
    return {
        "status": "success",
        "current_leader": leader.get("result", "unknown") if leader else "unknown",
    }


if __name__ == "__main__":
    host = os.getenv("API_HOST")
    port = os.getenv("API_PORT")

    if not host or not port:
        raise ValueError("API_HOST and API_PORT environment variables are not set!")

    uvicorn.run(app, host=host, port=int(port))
