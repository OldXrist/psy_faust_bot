from os import getenv
from dotenv import load_dotenv

from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message

from filters.admin import IsAdminFilter

# Create a router for command handlers
router = Router()

load_dotenv()
ADMIN_IDS = list(map(int, getenv("ADMIN_IDS").split(',')))


@router.message(CommandStart(), IsAdminFilter(ADMIN_IDS))
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Добро пожаловать, {html.bold(message.from_user.first_name)}!"
                         f"\n\nЯ ваш личный ИИ-ассистент, чем я могу вам помочь?")


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Здавствуйте, {html.bold(message.from_user.first_name)}!"
                         f"\n\nК сожалению, вы не авторизованы для использования этого бота."
                         f"\n\nЕсли вы считаете, что это ошибка, свяжитесь с администратором.")
