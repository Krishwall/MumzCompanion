import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "dummy"),
    base_url=os.getenv("OPENAI_BASE_URL")
)
MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

def extract_intent(query, language):
    if not query:
        return {"concern": "", "budget": None, "category": ""}
    prompt = f"""
    Extract intent from the user query. The language is {language}.
    Extract:
    - concern (str): What is the main issue or need (e.g., "back pain", "teething"). Empty if none.
    - budget (float or null): Any budget mentioned in AED. Null if not mentioned.
    - category (str): The product category they might be looking for. Empty if none.
    Return JSON format: {{"concern": "", "budget": null, "category": ""}}
    Query: "{query}"
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print("EXCEPTION:", e)
        return {"concern": "", "budget": None, "category": ""}

print(extract_intent("Need luxury stroller under 10 AED", "en"))
