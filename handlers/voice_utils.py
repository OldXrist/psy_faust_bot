import logging
import sys
import os
import groq

from aiogram import types
from dotenv import load_dotenv
from os import getenv

from pydub import AudioSegment


load_dotenv()
CONTEXT = getenv("CONTEXT")
GROQ_API_KEY = getenv("GROQ_API_KEY")

client = groq.Groq(
    api_key=GROQ_API_KEY,
)

if not CONTEXT:
    raise ValueError("CONTEXT is not set in the .env file")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the .env file")

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


# Directory to save temporary files
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)


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


async def transcribe_audio_with_groq(file_path: str) -> str:
    """Send the audio file to Groq Whisper API for transcription."""
    with open(file_path, "rb") as audio_file:
        # Create a transcription of the audio file
        transcription = client.audio.transcriptions.create(
            file=(file_path, audio_file.read()),  # Required audio file
            model="whisper-large-v3-turbo",  # Required model to use for transcription
            response_format="json",  # Optional
            language="ru",  # Optional
            temperature=0.0  # Optional
        )
        return transcription.text
