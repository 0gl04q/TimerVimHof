from aiogram.types import Update

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager
import logging

from tg_bot.bot import bot, dp

from app.config import get_webhook_url
from app.users.routers.auth import router as auth_router
from app.users.routers.users import router as users_router
from app.trainings.routers import router as training_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_url = get_webhook_url()
    await bot.set_webhook(
        url=webhook_url,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True
    )
    logging.info(f'Webhook set to {webhook_url}')
    yield
    await bot.delete_webhook()
    logging.info('Webhook deleted')


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.post('/webhook')
async def webhook(request: Request) -> None:
    logging.info('Received webhook request')
    update_data = await request.json()
    update = Update(**update_data)
    await dp.feed_update(bot, update)
    logging.info('Updates processed')


app.include_router(training_router)

app.include_router(auth_router)
app.include_router(users_router)
