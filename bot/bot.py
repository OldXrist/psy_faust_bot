import asyncio
import logging
from os import getenv

from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

# Import routers from handlers
from handlers.admin import router as admin_router
from handlers.commands import router as commands_router
from handlers.echo import router as echo_router

# Load environment variables
load_dotenv()

# Bot token
BOT_TOKEN = getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in the .env file")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
    # Initialize bot and dispatcher
    session = AiohttpSession()
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)
    dp = Dispatcher()

    # Include all routers
    dp.include_router(admin_router)
    dp.include_router(commands_router)
    dp.include_router(echo_router)

    logger.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Error occurred: {e}")
