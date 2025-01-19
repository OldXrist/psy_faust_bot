import asyncio
import logging
import sys
from os import getenv

from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from handlers.groq import router as groq_router

# Load environment variables from .env file
load_dotenv()

# Bot token can be obtained via https://t.me/BotFather
BOT_TOKEN = getenv("BOT_TOKEN")


if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in the .env file")


# Initialize logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

# Initialize Dispatcher
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}! Ask me anything.")


async def main() -> None:
    # Initialize Bot instance with an aiohttp session
    session = AiohttpSession()
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)
    dp.include_routers(groq_router, )
    # Start polling updates
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logger.info("Starting bot...")
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Error occurred: {e}")
