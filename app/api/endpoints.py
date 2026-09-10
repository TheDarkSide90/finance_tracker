from fastapi import APIRouter, HTTPException, status

from app.schemas.schemas import (
    Transaction, TransactionCreate, TransactionUpdate
)

router = APIRouter()

transactions: list[Transaction] = []


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


@router.get('/transactions')
async def get_transactions():
    return transactions


@router.post('/transactions')
async def create_transaction(
    transaction: TransactionCreate,
):
    new_transaction = Transaction(
        id=len(transactions) + 1,
        description=transaction.description,
        amount=transaction.amount,
        category=transaction.category,
    )
    transactions.append(new_transaction)
    return new_transaction


@router.get('/transactions/{transaction_id}')
async def get_transaction(transaction_id: int):
    for trans in transactions:
        if trans.id == transaction_id:
            return trans
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Транзакция не найдена',
    )


@router.delete('/transactions/{transaction_id}')
async def delete_transaction(transaction_id: int):
    for trans in transactions:
        if trans.id == transaction_id:
            transactions.remove(trans)
            return trans
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Транзакция не найдена'
    )


@router.put('/transactions/{transaction_id}')
async def update_transaction(
    transaction_id: int,
    transaction: TransactionCreate,
):
    for i, trans in enumerate(transactions):
        if trans.id == transaction_id:
            new_transaction = Transaction(
                id=trans.id,
                description=transaction.description,
                amount=transaction.amount,
                category=transaction.category,
            )
            transactions[i] = new_transaction

            return new_transaction

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Транзакция не найдена'
    )


@router.patch('/transactions/{transaction_id}')
async def patch_transaction(
    transaction_id: int,
    transaction: TransactionUpdate
):
    for trans in transactions:
        if trans.id == transaction_id:
            updates = transaction.model_dump(exclude_unset=True)
            for field, value in updates.items():
                setattr(trans, field, value)
            return trans
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Транзакция не найдена'
        )
