from aiogram import Router
from aiogram.types import Message

# Create a router for echo handlers
router = Router()


@router.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")
