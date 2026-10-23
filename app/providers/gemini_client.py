"""Shared Gemini client.

One lazily created client for the whole app, plus `generate_json`, which
asks Gemini for schema-constrained JSON instead of parsing free text, and
retries rate limits and server errors with exponential backoff.
"""

from functools import lru_cache
from typing import TypeVar

from google import genai
from google.genai import types
from google.genai.errors import APIError
from pydantic import BaseModel
from tenacity import retry
from tenacity import retry_if_exception
from tenacity import stop_after_attempt
from tenacity import wait_exponential

from app import settings

MODEL_TEXT = settings.GEMINI_TEXT_MODEL
MODEL_IMAGE = settings.GEMINI_IMAGE_MODEL

T = TypeVar("T", bound=BaseModel)

RETRYABLE_STATUS = {429, 500, 502, 503, 504}


@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    if not settings.GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(
        api_key=settings.GEMINI_API_KEY,
    )


def is_retryable(exc: BaseException) -> bool:
    return (
        isinstance(exc, APIError)
        and exc.code in RETRYABLE_STATUS
    )


def is_quota_error(exc: BaseException) -> bool:
    return isinstance(exc, APIError) and exc.code == 429


gemini_retry = retry(
    retry=retry_if_exception(is_retryable),
    stop=stop_after_attempt(settings.GEMINI_MAX_RETRIES),
    wait=wait_exponential(multiplier=2, min=2, max=30),
    reraise=True,
)


@gemini_retry
def generate_json(
    prompt: str,
    schema: type[T],
    model: str = MODEL_TEXT,
) -> T:
    """Generate a response that is guaranteed to validate against `schema`."""

    response = get_client().models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
        ),
    )

    if isinstance(response.parsed, schema):
        return response.parsed

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return schema.model_validate_json(response.text)
