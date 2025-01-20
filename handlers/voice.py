import logging
import sys
import os
import groq

from aiogram import Router, types, F
from dotenv import load_dotenv
from os import getenv

from pydub import AudioSegment
import ffmpeg

from filters.admin import IsAdminFilter

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

# Create a router
router = Router()

# Directory to save temporary files
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)


@router.message(F.voice)
async def handle_voice_message(message: types.Message):
    """Handles voice messages, transcribes them, and sends the text to the user."""
    user_id = message.from_user.id
    voice: types.Voice = message.voice

    try:
        # Step 1: Download and convert the voice message to WAV
        wav_file_path = await download_and_convert_voice(voice, user_id)

        # Step 2: Transcribe the audio using OpenAI Whisper API
        transcription = await transcribe_audio_with_openai(wav_file_path)

        # Step 3: Reply with the transcription
        await message.reply(f"Transcription:\n\n{transcription}")
    except Exception as e:
        await message.reply(f"Sorry, something went wrong while processing your voice message: {e}")


async def download_and_convert_voice(voice: types.Voice, user_id: int) -> str:
    """Downloads a Telegram voice message and converts it to WAV format."""
    bot = voice.bot
    file_info: types.file.File = await bot.get_file(voice.file_id)

    # Define file paths
    ogg_path = f"{TEMP_DIR}/{user_id}_voice.ogg"
    wav_path = f"{TEMP_DIR}/{user_id}_voice.wav"

    # Download the OGG file
    await bot.download_file(file_info.file_path, destination=ogg_path)

    # Convert OGG to WAV using pydub
    audio = AudioSegment.from_file(ogg_path, format="ogg")
    audio.export(wav_path, format="wav")

    # Remove the OGG file to save space
    os.remove(ogg_path)

    return wav_path


async def transcribe_audio_with_openai(file_path: str) -> str:
    """Send the audio file to OpenAI Whisper API for transcription."""
    with open(file_path, "rb") as audio_file:
        # Create a transcription of the audio file
        transcription = client.audio.transcriptions.create(
            file=(file_path, audio_file.read()),  # Required audio file
            model="whisper-large-v3-turbo",  # Required model to use for transcription
            prompt=CONTEXT,  # Optional
            response_format="json",  # Optional
            language="ru",  # Optional
            temperature=0.0  # Optional
        )
        return transcription.text

'''
@router.message(F.text, IsAdminFilter(ADMIN_IDS))
async def groq_answer_handler(message: types.Message) -> None:
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

    except groq.RateLimitError:
        logger.error(f"Rate limit error")
        await message.answer("Вы достигли лимит запросов, попробуйте позже.")

    except Exception as e:
        logger.error(f"Groq API error: {e}")
        await message.answer("Извините, я не смогла обработать ваш запрос. Пожалуйста, попробуйте снова позже.")
'''