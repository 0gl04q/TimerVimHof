from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.users.dao import UserDAO

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    # """
    # Обрабатывает команду /start.
    # """
    # user = await UserDAO.find_one_or_none(telegram_id=message.from_user.id)
    #
    # if not user:
    #     await UserDAO.add(
    #         telegram_id=message.from_user.id,
    #         first_name=message.from_user.first_name,
    #         username=message.from_user.username
    #     )

    await message.answer("Здравствуй пользователь!")
