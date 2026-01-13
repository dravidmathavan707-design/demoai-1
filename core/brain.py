from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL
import httpx

client = genai.Client(api_key=GEMINI_API_KEY)

def think(conversation):
    prompt = ""

    for msg in conversation:
        role = msg["role"]
        content = msg["content"]

        if role == "user":
            prompt += f"User: {content}\n"
        elif role == "assistant":
            prompt += f"AI: {content}\n"

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        return response.text.strip()
    except httpx.ConnectError:
        return "Error: Unable to connect to the API. Please check your internet connection."
    except Exception as e:
        return f"Error: {str(e)}"
