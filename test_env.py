import os
from dotenv import load_dotenv

load_dotenv(".env")

key = os.getenv("PEXELS_API_KEY")

print("Loaded:", key is not None)

if key:
    print("Length:", len(key))
    print("First 10:", key[:10])
