import os

# Get API key from environment variable (for Render) or use default
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyADYZSFJqV4IL1r-hhyOOatrPUk478bQVM")
GEMINI_MODEL = "models/gemini-flash-latest"
MEMORY_FILE = "data/memory.json"
