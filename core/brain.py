from google import genai
from google.genai import types
from config import GEMINI_API_KEYS, GEMINI_MODEL
import httpx

def think(conversation):
    prompt = ""

    for msg in conversation:
        role = msg["role"]
        content = msg["content"]

        if role == "user":
            prompt += f"User: {content}\n"
        elif role == "assistant":
            prompt += f"AI: {content}\n"

    # Try each API key until one works
    for i, api_key in enumerate(GEMINI_API_KEYS, 1):
        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )
            return response.text.strip()
        except httpx.ConnectError:
            return "Error: Unable to connect to the API. Please check your internet connection."
        except Exception as e:
            error_str = str(e)
            # If it's a permission/quota error, try next key
            if "403" in error_str or "PERMISSION_DENIED" in error_str or "quota" in error_str.lower():
                if i < len(GEMINI_API_KEYS):
                    print(f"API Key {i} failed, trying Key {i+1}...")
                    continue
                else:
                    return f"Error: All API keys have been exhausted. {error_str}"
            else:
                return f"Error: {error_str}"
