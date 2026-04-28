import json
import chromadb
from sentence_transformers import SentenceTransformer

# Load model and client once
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()

# Adjacent stages — products from nearby stages are still relevant
ADJACENT_STAGES = {
    "early_pregnancy": ["mid_pregnancy"],
    "mid_pregnancy": ["early_pregnancy", "late_pregnancy"],
    "late_pregnancy": ["mid_pregnancy"],
    "newborn": ["infant", "late_pregnancy"],
    "infant": ["newborn", "older_infant"],
    "older_infant": ["infant"],
}

def search_products(intent_query, stage_bucket, budget=None, category=None, top_k=5):
    try:
        collection = client.get_collection("products")
    except Exception:
        import sys
        sys.path.append("d:/MumzCompanion")
        from embeddings.build_index import build_index
        build_index()
        collection = client.get_collection("products")

    embedding = model.encode(intent_query if intent_query else "products").tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=30  # fetch more for better ranking
    )

    scored_products = []

    if not results or not results["documents"]:
        return []

    adjacent = ADJACENT_STAGES.get(stage_bucket, [])

    for doc, dist in zip(results["documents"][0], results["distances"][0]):
        item = json.loads(doc)

        price = item.get("price_aed", 0)

        # -----------------------------
        # HARD FILTER (budget only)
        # -----------------------------
        if budget is not None and price > budget:
            continue

        # -----------------------------
        # SCORING
        # -----------------------------
        semantic_score = max(0.0, 1.0 - dist)

        rule_score = 0.0

        # 🏷️ Stage boost (soft, not a hard filter)
        product_stages = item.get("stage_tags", [])
        if stage_bucket in product_stages:
            rule_score += 0.3  # exact stage match
        elif any(s in product_stages for s in adjacent):
            rule_score += 0.15  # adjacent stage — still relevant
        # else: no boost, but product is NOT discarded

        # 🎯 Category boost
        if category and category.lower() in " ".join(item.get("tags", [])).lower():
            rule_score += 0.25

        # 💸 Budget closeness boost
        if budget:
            budget_score = 1 - abs(price - budget) / max(budget, 1)
            rule_score += max(0, budget_score) * 0.2

        # 🧠 Tag relevance boost (intent keywords)
        if intent_query:
            for word in intent_query.lower().split():
                if word in " ".join(item.get("tags", [])).lower():
                    rule_score += 0.05

        # 🧮 Final score
        final_score = semantic_score + rule_score

        scored_products.append({
            "item": item,
            "score": round(final_score, 3),
            "semantic_score": round(semantic_score, 3),
            "rule_score": round(rule_score, 3)
        })

    # -----------------------------
    # SORTING
    # -----------------------------
    scored_products.sort(key=lambda x: x["score"], reverse=True)

    return scored_products[:top_k]