from pydantic import BaseModel, Field


class CalculationCreate(BaseModel):
    expression: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Математическое выражение",
    )
    result: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Результат выражения",
    )
