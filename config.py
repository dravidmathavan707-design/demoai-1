import os

# Get THREE API keys from environment variables (NEVER hardcode API keys!)
# Falls back to next key if current one fails
GEMINI_API_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3"),
]

# Filter out None values (keys not set)
GEMINI_API_KEYS = [key for key in GEMINI_API_KEYS if key]

if not GEMINI_API_KEYS:
    raise ValueError("At least one GEMINI_API_KEY_1/2/3 environment variable must be set!")

GEMINI_MODEL = "models/gemini-flash-latest"
MEMORY_FILE = "data/memory.json"
