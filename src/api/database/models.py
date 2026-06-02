from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Expression(Base):  # type: ignore
    __tablename__ = "expressions"

    id = Column(Integer, primary_key=True, index=True)
    raw_expression = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    answers = relationship(
        "Answer", back_populates="expression", cascade="all, delete-orphan"
    )


class Answer(Base):  # type: ignore
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    expression_id = Column(
        Integer, ForeignKey("expressions.id", ondelete="CASCADE"), nullable=False
    )
    result = Column(String, nullable=False)
    votes_count = Column(Integer, default=1, nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    expression = relationship("Expression", back_populates="answers")

    __table_args__ = (
        UniqueConstraint("expression_id", "result", name="uix_expression_result"),
    )
