from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint, String, Integer, DateTime
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, CommonMixin


class Transaction(CommonMixin, Base):
    description: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    amount: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    category: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    __table_args__ = (
        CheckConstraint('amount > 0', name='positive_amount'),
    )
