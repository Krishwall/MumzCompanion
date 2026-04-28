import json
import chromadb
from sentence_transformers import SentenceTransformer

# Load model and client once
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()

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

    for doc, dist in zip(results["documents"][0], results["distances"][0]):
        item = json.loads(doc)

        # -----------------------------
        # FILTERING
        # -----------------------------
        if stage_bucket not in item.get("stage_tags", []):
            continue

        price = item.get("price_aed", 0)

        if budget is not None and price > budget:
            continue

        # -----------------------------
        # SCORING
        # -----------------------------
        semantic_score = max(0.0, 1.0 - dist)

        rule_score = 0.0

        # 🎯 Category boost
        if category and category.lower() in " ".join(item.get("tags", [])).lower():
            rule_score += 0.25

        # 💸 Budget closeness boost
        if budget:
            # closer to budget → higher score
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