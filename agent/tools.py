import os
import json
from openai import OpenAI
from langdetect import detect
from dotenv import load_dotenv

load_dotenv()

# Groq provides an OpenAI-compatible API, so we use the standard OpenAI client.
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)
# Use a fast Groq model instead of gpt-3.5-turbo
MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")

def detect_language(text):
    try:
        lang = detect(text)
        return "ar" if lang == "ar" else "en"
    except:
        return "en"

def classify_safety(query):
    if not query:
         return {"is_medical": False, "severity": "none"}
    prompt = f"""
    Analyze the following user query in the context of a pregnancy/baby product recommendation app.

    Classify severity as:
    - "none": Not medical at all (e.g., "I need a stroller", "show me cribs").
    - "mild": Common pregnancy/postnatal discomforts where PRODUCT recommendations are appropriate (e.g., "back pain" → support pillow, "swollen feet" → compression socks, "trouble sleeping" → maternity pillow). These are NOT medical emergencies.
    - "urgent": Genuinely dangerous medical concerns that require a doctor (e.g., "my baby has a high fever", "bleeding during pregnancy", "what medication should I take", "my baby won't stop vomiting").

    Return JSON format exactly like: {{"is_medical": true/false, "severity": "none"|"mild"|"urgent"}}
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
        return {"is_medical": False, "severity": "none"}

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
        return {"concern": "", "budget": None, "category": ""}

def generate_insight(stage_bucket, week_or_month, language):
    prompt = f"""
    You are a helpful companion for mothers.
    The user is currently at stage: {stage_bucket}.
    Exact week or month: {week_or_month}.
    Language to respond in: {language} (en or ar).
    
    Generate a short 3-4 sentence insight about what is happening at this stage, and a short heads-up (1 sentence).
    Return JSON format: {{"headline": "Week X: ...", "body": "...", "heads_up": "..."}}
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": prompt}],
            response_format={"type": "json_object"}
        )
        res = json.loads(response.choices[0].message.content)
        res["stage_bucket"] = stage_bucket
        res["exact_week_or_month"] = week_or_month
        return res
    except Exception as e:
        return {
            "stage_bucket": stage_bucket,
            "exact_week_or_month": week_or_month,
            "headline": f"Stage: {stage_bucket}",
            "body": "Welcome to this new stage of your journey.",
            "heads_up": ""
        }