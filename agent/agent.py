from agent.stage_calculator import get_stage
from agent.tools import classify_safety, extract_intent, generate_insight, detect_language
from agent.rag import search_products
from agent.schemas import MumzCompanionResponse, WeeklyInsight, ProductResult

def run_agent(user_input, date_input):
    lang = detect_language(user_input)

    # -----------------------------
    # STAGE DETECTION
    # -----------------------------
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

    # -----------------------------
    # SAFETY CHECK
    # -----------------------------
    safety = classify_safety(user_input)

    # Only refuse for genuinely urgent medical concerns.
    # Mild discomforts (back pain, swelling, etc.) are fine — we recommend products for those.
    if safety.get("is_medical") and safety.get("severity") == "urgent":
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
            refusal_reason="This sounds like a serious medical concern. Please consult your doctor or pediatrician.",
            disclaimer="We do not provide medical advice."
        )

    # Track mild medical flag so we can add a disclaimer to the response
    is_mild_medical = safety.get("is_medical") and safety.get("severity") == "mild"

    # -----------------------------
    # INTENT EXTRACTION
    # -----------------------------
    intent = extract_intent(user_input, lang)
    budget = intent.get("budget")
    category = intent.get("category")
    concern = intent.get("concern")

    # -----------------------------
    # INSIGHT GENERATION
    # -----------------------------
    insight_data = generate_insight(stage_bucket, exact_time, lang)
    insight = WeeklyInsight(**insight_data)

    # -----------------------------
    # PRODUCT SEARCH (UPGRADED)
    # -----------------------------
    raw_products = search_products(
        user_input,
        stage_bucket,
        budget=budget,
        category=category
    )

    products = []

    for item in raw_products:
        p = item["item"]

        # Handle both old + new scoring
        score = item.get("score", item.get("confidence", 0))

        # 🌍 Language-aware naming
        name = p.get("name_en") if lang == "en" else p.get("name_ar", p.get("name_en"))

        # 🎯 Dynamic reason
        if concern:
            reason = f"Helpful for {concern}"
        elif category:
            reason = f"Matches {category}"
        else:
            reason = "Fits your current stage"

        products.append(ProductResult(
            id=p["id"],
            name=name,
            price_aed=p.get("price_aed", 0.0),
            relevance_reason=reason,
            confidence=round(score, 2)
        ))

    # -----------------------------
    # FALLBACK IF NO PRODUCTS
    # -----------------------------
    follow_up = "Would you like to explore more products for this stage?"

    if not products:
        follow_up = "I couldn’t find a perfect match. Want suggestions based on comfort, sleep, or budget?"

    # -----------------------------
    # FINAL RESPONSE
    # -----------------------------
    return MumzCompanionResponse(
        input_language=lang,
        stage_bucket=stage_bucket,
        timeline_insight=insight,
        products=products,
        follow_up_prompt=follow_up,
        refused=False,
        disclaimer="These are product suggestions for comfort — please consult your doctor if symptoms persist." if is_mild_medical else None
    )