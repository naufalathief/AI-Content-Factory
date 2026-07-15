import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv(
    "GEMINI_API_KEY",
)

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured."
    )

MODEL_TEXT = "gemini-2.5-flash"

MODEL_IMAGE = "gemini-2.5-flash-image"

client = genai.Client(
    api_key=API_KEY,
)