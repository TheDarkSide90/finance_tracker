from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import auth_backend, fastapi_users
from app.schemas.schemas import (
    Transaction, TransactionCreate, TransactionUpdate
)
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.models.transaction import Transaction as TransactionModel

SessionDep = Annotated[
    AsyncSession,
    Depends(get_async_session)
]

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)

users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
users_router.routes = [
    route for route in users_router.routes if route.name != 'users:delete_user'
]

router.include_router(
    users_router,
    prefix='/users',
    tags=['users'],
)


@router.get('/')
async def main_page():
    return {'message': 'FinTrack API'}


@router.get('/health')
async def health():
    return {'status': 'ok'}


@router.get('/about')
async def about():
    return {
        'name': 'FinTrack',
        'version': '1.0.0',
        'description': 'Personal finance analytics API'
    }


@router.get(
        '/transactions',
        response_model=list[Transaction],
    )
async def get_transactions(
    session: SessionDep
):
    result = await session.execute(
        select(TransactionModel)
    )
    transactions = result.scalars().all()

    return transactions


@router.post(
        '/transactions',
        response_model=Transaction,
    )
async def create_transaction(
    transaction: TransactionCreate,
    session: SessionDep
):
    new_transaction = TransactionModel(
        description=transaction.description,
        amount=transaction.amount,
        category=transaction.category,
    )
    session.add(new_transaction)
    await session.commit()
    await session.refresh(new_transaction)

    return new_transaction


@router.get(
        '/transactions/{transaction_id}',
        response_model=Transaction,
    )
async def get_transaction(
    transaction_id: int,
    session: SessionDep
):
    result = await session.execute(
        select(TransactionModel).where(TransactionModel.id == transaction_id)
    )
    transaction = result.scalar_one_or_none()
    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Транзакция не найдена',
        )

    return transaction


@router.delete(
        '/transactions/{transaction_id}',
        response_model=Transaction,
    )
async def delete_transaction(
    transaction_id: int,
    session: SessionDep
):
    result = await session.execute(
        select(TransactionModel).where(TransactionModel.id == transaction_id)
    )
    transaction = result.scalar_one_or_none()
    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Транзакция не найдена',
        )
    await session.delete(transaction)
    await session.commit()

    return transaction


@router.put(
        '/transactions/{transaction_id}',
        response_model=Transaction,
    )
async def update_transaction(
    transaction_id: int,
    transaction: TransactionCreate,
    session: SessionDep
):
    result = await session.execute(
        select(TransactionModel).where(
            TransactionModel.id == transaction_id
        )
    )
    db_transaction = result.scalar_one_or_none()
    if db_transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Транзакция не найдена'
        )
    db_transaction.description = transaction.description
    db_transaction.amount = transaction.amount
    db_transaction.category = transaction.category

    await session.commit()

    return db_transaction


@router.patch(
        '/transactions/{transaction_id}',
        response_model=Transaction,
    )
async def patch_transaction(
    transaction_id: int,
    transaction: TransactionUpdate,
    session: SessionDep
):
    result = await session.execute(
        select(TransactionModel).where(
            TransactionModel.id == transaction_id
        )
    )
    db_transaction = result.scalar_one_or_none()
    if db_transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Транзакция не найдена'
        )
    updates = transaction.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(db_transaction, field, value)

    await session.commit()

    return db_transaction
