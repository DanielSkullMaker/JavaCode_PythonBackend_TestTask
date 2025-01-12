from fastapi import APIRouter
from app.api.wallet import router as wallet_router


main_router = APIRouter(
    prefix='/api/v1'
)
main_router.include_router(
    wallet_router, prefix='/wallets', tags=['Кошелек']
)
