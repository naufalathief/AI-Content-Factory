from pathlib import Path
from urllib.parse import quote
import random
import time

import requests


BASE_URL = "https://image.pollinations.ai/prompt/"

MODEL = "flux"

WIDTH = 1080
HEIGHT = 1920

TIMEOUT = 180
MAX_RETRY = 5


def clean_prompt(prompt: str) -> str:
    """
    Normalize whitespace only.
    Do NOT truncate prompt.
    """
    return " ".join(prompt.split())


def build_url(prompt: str) -> str:

    prompt = clean_prompt(prompt)

    seed = random.randint(1, 2_147_483_647)

    return (
        f"{BASE_URL}"
        f"{quote(prompt, safe='')}"
        f"?width={WIDTH}"
        f"&height={HEIGHT}"
        f"&model={MODEL}"
        f"&seed={seed}"
        "&nologo=true"
        "&enhance=true"
        "&safe=false"
    )


def download(url: str, output_path: str):

    response = requests.get(
        url,
        timeout=TIMEOUT,
        headers={
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )

    response.raise_for_status()

    output = Path(output_path)

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.write_bytes(response.content)


def generate_image(
    prompt: str,
    output_path: str,
):

    last_error = None

    for attempt in range(MAX_RETRY):

        url = build_url(prompt)

        try:

            print(
                f"Provider : Pollinations ({attempt + 1}/{MAX_RETRY})"
            )

            print(f"Seed     : {url.split('seed=')[1].split('&')[0]}")
            print(f"Prompt   : {len(prompt)} chars")

            download(
                url,
                output_path,
            )

            return

        except Exception as exc:

            last_error = exc

            print(f"Pollinations Error : {exc}")

            if attempt != MAX_RETRY - 1:
                time.sleep(3)

    raise last_error