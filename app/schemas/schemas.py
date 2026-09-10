from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, PositiveInt


class TransactionCreate(BaseModel):
    description: str
    amount: PositiveInt
    category: str


class TransactionUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[PositiveInt] = None
    category: Optional[str] = None


class Transaction(TransactionCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
