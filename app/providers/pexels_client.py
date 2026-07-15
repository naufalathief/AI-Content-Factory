import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PEXELS_API_KEY")

BASE_URL = "https://api.pexels.com/videos/search"


def search_videos(
    query: str,
    per_page: int = 15,
):

    response = requests.get(
        BASE_URL,
        headers={
            "Authorization": API_KEY,
        },
        params={
            "query": query,
            "per_page": per_page,
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()