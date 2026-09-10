from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.endpoints import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    print('Приложение завершило работу')

app = FastAPI(lifespan=lifespan)

app.include_router(router)
