import os

import requests
from dotenv import load_dotenv

load_dotenv()

response = requests.get(
    "https://api.pexels.com/videos/search",
    headers={
        "Authorization": os.getenv("PEXELS_API_KEY"),
    },
    params={
        "query": "technology",
        "per_page": 1,
    },
)

print(response.status_code)
print(response.text)
