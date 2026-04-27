from agent.stage_calculator import get_stage
from agent.tools import classify_safety, extract_intent, generate_insight, detect_language
from agent.rag import search_products
from agent.schemas import MumzCompanionResponse, WeeklyInsight, ProductResult

def run_agent(user_input, date_input):
    lang = detect_language(user_input)

    stage_bucket, exact_time = get_stage(date_input)

    if stage_bucket == "unknown":
        return MumzCompanionResponse(
            input_language=lang,
            stage_bucket="unknown",
            timeline_insight=WeeklyInsight(
                stage_bucket="unknown",
                exact_week_or_month=0,
                headline="Date required",
                body="Please provide a valid due date or birth date (YYYY-MM-DD)."
            ),
            products=[],
            follow_up_prompt="",
            refused=True,
            refusal_reason="Invalid date format."
        )

    safety = classify_safety(user_input)
    if safety.get("is_medical") and safety.get("severity") in ["mild", "urgent"]:
        return MumzCompanionResponse(
            input_language=lang,
            stage_bucket=stage_bucket,
            timeline_insight=WeeklyInsight(
                stage_bucket=stage_bucket,
                exact_week_or_month=exact_time,
                headline="Safety First",
                body="This query seems medical in nature."
            ),
            products=[],
            follow_up_prompt="",
            refused=True,
            refusal_reason="This sounds like a medical concern. Please consult your pediatrician.",
            disclaimer="We do not provide medical advice."
        )

    intent = extract_intent(user_input, lang)
    budget = intent.get("budget")

    insight_data = generate_insight(stage_bucket, exact_time, lang)
    insight = WeeklyInsight(**insight_data)

    raw_products = search_products(user_input, stage_bucket, budget=budget)

    products = []
    for item in raw_products:
        p = item["item"]
        conf = item["confidence"]
        products.append(ProductResult(
            id=p["id"],
            name=p.get("name_en") if lang == "en" else p.get("name_ar", p.get("name_en")),
            price_aed=p.get("price_aed", 0.0),
            relevance_reason="Matches your current stage and needs.",
            confidence=round(conf, 2)
        ))

    return MumzCompanionResponse(
        input_language=lang,
        stage_bucket=stage_bucket,
        timeline_insight=insight,
        products=products,
        follow_up_prompt="Would you like to explore more products for this stage?",
        refused=False
    )