"""Pollinations image fallback.

The free tier allows 1 image every 45 seconds per IP, answers faster
requests with HTTP 402 (code FREE_LIMIT, "Retry after Ns") and stamps a
"pollinations.ai" watermark in the corner even with nologo=true. Without a
key we space requests out ourselves; with POLLINATIONS_TOKEN set there is
no rate limit and no watermark.
"""

import os
import random
import re
import time
from pathlib import Path
from urllib.parse import quote

import requests

BASE_URL = "https://image.pollinations.ai/prompt/"

MODEL = "flux"

WIDTH = 1080
HEIGHT = 1920

TIMEOUT = 180
MAX_RETRY = 5

FREE_INTERVAL = 46  # seconds between requests on the free tier

TOKEN = os.getenv("POLLINATIONS_TOKEN", "").strip()

_last_request = 0.0


def clean_prompt(prompt: str) -> str:
    """Normalize whitespace only. Do NOT truncate the prompt."""
    return " ".join(prompt.split())


def build_url(prompt: str, seed: int) -> str:

    return (
        f"{BASE_URL}"
        f"{quote(clean_prompt(prompt), safe='')}"
        f"?width={WIDTH}"
        f"&height={HEIGHT}"
        f"&model={MODEL}"
        f"&seed={seed}"
        "&nologo=true"
        "&enhance=true"
        "&safe=false"
    )


def retry_after(response: requests.Response) -> float | None:
    """Seconds to wait when the free limit was hit, else None."""

    if response.status_code not in (402, 429):
        return None

    match = re.search(r"Retry after (\d+)", response.text)

    return float(match.group(1)) + 1 if match else FREE_INTERVAL


def _throttle():

    global _last_request

    if TOKEN:
        return

    wait = FREE_INTERVAL - (time.monotonic() - _last_request)

    if wait > 0:
        print(f"Pollinations free tier: waiting {wait:.0f}s")
        time.sleep(wait)

    _last_request = time.monotonic()


def generate_image(
    prompt: str,
    output_path: str,
):

    headers = {"Cache-Control": "no-cache"}

    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    seed = random.randint(1, 2_147_483_647)

    url = build_url(prompt, seed)

    last_error: Exception | None = None

    for attempt in range(MAX_RETRY):

        _throttle()

        print(f"Provider : Pollinations ({attempt + 1}/{MAX_RETRY}) seed={seed}")

        try:

            response = requests.get(url, timeout=TIMEOUT, headers=headers)

        except requests.RequestException as exc:

            last_error = exc
            print(f"Pollinations Error : {exc}")
            continue

        wait = retry_after(response)

        if wait is not None:
            last_error = RuntimeError(f"Pollinations rate limit ({response.status_code})")
            print(f"Pollinations limit : retry in {wait:.0f}s")
            time.sleep(wait)
            continue

        if not response.ok:
            last_error = RuntimeError(f"Pollinations HTTP {response.status_code}")
            print(f"Pollinations Error : HTTP {response.status_code}")
            continue

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(response.content)

        return

    raise RuntimeError("Pollinations failed.") from last_error
