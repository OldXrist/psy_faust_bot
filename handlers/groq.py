import logging
import sys
import groq

from aiogram import Router, types, F
from dotenv import load_dotenv
from os import getenv

from filters.admin import IsAdminFilter
from handlers.voice_utils import download_and_convert_voice, transcribe_audio_with_groq

router = Router()

load_dotenv()
CONTEXT = getenv("CONTEXT")
GROQ_API_KEY = getenv("GROQ_API_KEY")
ADMIN_IDS = list(map(int, getenv("ADMIN_IDS").split(',')))


client = groq.Groq(
    api_key=GROQ_API_KEY,
)

if not CONTEXT:
    raise ValueError("CONTEXT is not set in the .env file")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the .env file")
if not ADMIN_IDS:
    raise ValueError("ADMIN_IDS is not set in the .env file")

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


@router.message(F.text, IsAdminFilter(ADMIN_IDS))
async def groq_answer_handler(message: types.Message) -> None:
    """
    Handler to send the user's question to OpenAI API and return the answer.
    """
    await groq_api_request(message.text, message)


@router.message(F.voice, IsAdminFilter(ADMIN_IDS))
async def handle_voice_message(message: types.Message):
    """Handles voice messages, transcribes them, and sends the text to the user."""
    user_id = message.from_user.id
    voice: types.Voice = message.voice

    try:
        # Step 1: Download and convert the voice message to WAV
        wav_file_path = await download_and_convert_voice(voice, user_id)

        # Step 2: Transcribe the audio using OpenAI Whisper API
        transcription = await transcribe_audio_with_groq(wav_file_path)

        # Step 3: Reply with the transcription
        await groq_api_request(transcription, message)

    except Exception as e:
        logger.error(f'Speech recognition error: {e}')
        await message.answer(f"Извините, что-то пошло не так при обработке вашего голосового сообщения.")


@router.message(IsAdminFilter(ADMIN_IDS))
async def other_content_handler(message: types.Message) -> None:
    await message.answer('К сожалению, я могу работать только с текстовым и голосовым контеном.'
                         '\n\nС чем еще я могу вам помочь?')


@router.message()
async def unauthorized_message_handler(message: types.Message) -> None:
    await message.answer('Ваш запрос не может быть обработан, поскольку вы не авторизованы.')


async def groq_api_request(prompt: str, message: types.Message) -> None:
    try:
        # Call Groq API with updated method
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": CONTEXT},
                {"role": "user", "content": prompt},
            ],
            model="llama-3.3-70b-versatile"
        )

        # Extract the assistant's response
        answer = response.choices[0].message.content

        # Send the response back to the user
        await message.answer(answer)

    except groq.RateLimitError:
        logger.error(f"Rate limit error")
        await message.answer("Вы достигли лимит запросов, попробуйте позже.")

    except Exception as e:
        logger.error(f"Groq API error: {e}")
        await message.answer("Извините, я не смогла обработать ваш запрос. Пожалуйста, попробуйте снова позже.")
