from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.models import Answer, Expression


class CalculatorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def calculate(self, expr: str) -> dict[str, str | int] | None:
        result = await self.session.execute(
            select(Expression).where(Expression.raw_expression == expr)
        )
        expression = result.scalar_one_or_none()

        if not expression:
            return None

        result = await self.session.execute(
            select(Answer)
            .where(Answer.expression_id == expression.id)
            .order_by(Answer.votes_count.desc())
            .limit(1)
        )
        winner = result.scalar_one_or_none()

        total_votes = await self.session.execute(
            select(func.sum(Answer.votes_count)).where(
                Answer.expression_id == expression.id
            )
        )
        total_votes = total_votes.scalar_one_or_none() or 0  # type: ignore

        return {
            "expression": expression.raw_expression,  # type: ignore
            "result": winner.result,  # type: ignore
            "total_votes": total_votes,  # type: ignore
        }

    async def teach(self, expression: str, expr_result: str) -> None:
        result = await self.session.execute(
            select(Expression).where(Expression.raw_expression == expression)
        )
        existing_expression = result.scalar_one_or_none()

        if existing_expression:
            expression_id = existing_expression.id
        else:
            new_expression = Expression(raw_expression=expression)
            self.session.add(new_expression)
            await self.session.flush()
            expression_id = new_expression.id

        stmt = pg_insert(Answer).values(
            expression_id=expression_id, result=expr_result, votes_count=1
        )

        upsert_stmt = stmt.on_conflict_do_update(
            index_elements=["expression_id", "result"],
            set_={"votes_count": Answer.votes_count + 1},
        )

        await self.session.execute(upsert_stmt)

    async def stats(self, expr: str) -> list[dict[str, str | int]] | None:
        result = await self.session.execute(
            select(Expression).where(Expression.raw_expression == expr)
        )
        expression = result.scalar_one_or_none()

        if not expression:
            return None

        result = await self.session.execute(
            select(Answer)
            .where(Answer.expression_id == expression.id)
            .order_by(Answer.votes_count.desc())
            .limit(5)
        )
        answers = result.scalars().all()

        return [
            {"result": answer.result, "votes_count": answer.votes_count}
            for answer in answers
        ]
