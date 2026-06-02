from pydantic import BaseModel, Field


class CalculationCreate(BaseModel):
    expression: str = Field(
        ...,
        pattern=r"^[0-9+\-*/().]+$",
        min_length=1,
        max_length=50,
        description="Математическое выражение",
    )
    result: str = Field(
        ...,
        pattern=r"^[0-9+\-*/().]+$",
        min_length=1,
        max_length=50,
        description="Результат выражения",
    )
