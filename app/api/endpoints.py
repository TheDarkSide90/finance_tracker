from fastapi import APIRouter

from app.schemas.schemas import Transaction

router = APIRouter()


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


@router.post('/transactions')
async def create_transaction(
    transaction: Transaction,
):
    return transaction
