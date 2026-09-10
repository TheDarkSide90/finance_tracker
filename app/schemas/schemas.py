from typing import Optional

from pydantic import BaseModel, PositiveInt


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
