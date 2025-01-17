from aiogram import Router
from aiogram.types import Message
from filters import IsAdminFilter

# Create a router for admin handlers
router = Router()

# Example admin user IDs
ADMIN_IDS = [438804925, 987654321]


@router.message(IsAdminFilter(admin_ids=ADMIN_IDS))
async def admin_only_handler(message: Message) -> None:
    await message.answer("You are an admin and can access this command.")
