import os
import sys
from pathlib import Path

# Tests never touch PostgreSQL or the real Gemini API.
os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("GEMINI_API_KEY", "test-key")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
