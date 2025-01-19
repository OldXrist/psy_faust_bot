import logging
import sys

from aiogram import Router
from aiogram.types import Message
from groq import Groq
from dotenv import load_dotenv
from os import getenv

from filters import IsAdminFilter

router = Router()

load_dotenv()
CONTEXT = getenv("CONTEXT")
GROQ_API_KEY = getenv("GROQ_API_KEY")
ADMIN_IDS = list(map(int, getenv("ADMIN_IDS").split(',')))


client = Groq(
    api_key=GROQ_API_KEY,
)

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the .env file")

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


@router.message(IsAdminFilter(ADMIN_IDS))
async def groq_answer_handler(message: Message) -> None:
    """
    Handler to send the user's question to OpenAI API and return the answer.
    """
    try:
        user_question = message.text

        # Call OpenAI API with updated method
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": CONTEXT},
                {"role": "user", "content": user_question},
            ],
            model="llama-3.3-70b-versatile"
        )

        # Extract the assistant's response
        answer = response.choices[0].message.content

        # Send the response back to the user
        await message.answer(answer)

    except Exception as e:
        logger.error(f"Groq API error: {e}")
        await message.answer("Sorry, I couldn't process your question. Please try again later.")


@router.message()
async def unauthorized_message_handler(message: Message) -> None:
    await message.answer('Ваш запрос не может быть обработан, поскольку вы не авторизованы.')

