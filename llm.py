import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-flash-latest")

def generate_response(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text

def extract_lead_info(user_input: str) -> dict:
    import json
    prompt = f"""
    Extract the following information from the user's input:
    - name
    - email
    - platform (e.g., YouTube, Instagram)

    If a piece of information is not present, set its value to null.
    Return ONLY a valid JSON object with the keys "name", "email", and "platform", and no markdown formatting or other text.

    User Input: {user_input}
    """
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())
    except Exception as e:
        print(f"Error extracting lead info: {e}")
        return {"name": None, "email": None, "platform": None}