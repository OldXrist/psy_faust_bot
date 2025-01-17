import asyncio
import logging
import sys
from os import getenv

from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

import openai
from aiogram import Bot, Dispatcher, html
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

# Load environment variables from .env file
load_dotenv()

# Bot token can be obtained via https://t.me/BotFather
BOT_TOKEN = getenv("BOT_TOKEN")
OPENAI_API_KEY = getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in the .env file")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the .env file")

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

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


@dp.message()
async def gpt_answer_handler(message: Message) -> None:
    """
    Handler to send the user's question to OpenAI API and return the answer.
    """
    try:
        user_question = message.text

        # Call OpenAI API with updated method
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_question},
            ]
        )

        # Extract the assistant's response
        answer = response.choices[0].message["content"]

        # Send the response back to the user
        await message.answer(answer)

    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        await message.answer("Sorry, I couldn't process your question. Please try again later.")


async def main() -> None:
    # Initialize Bot instance with an aiohttp session
    session = AiohttpSession()
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)

    # Start polling updates
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        logger.info("Starting bot...")
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Error occurred: {e}")
