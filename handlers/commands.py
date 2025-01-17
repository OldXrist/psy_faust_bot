from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message

# Create a router for command handlers
router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
