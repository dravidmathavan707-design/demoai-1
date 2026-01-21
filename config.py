import os

# Get API key from environment variable (NEVER hardcode API keys!)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set!")

GEMINI_MODEL = "models/gemini-flash-latest"
MEMORY_FILE = "data/memory.json"
