import json
import chromadb
from sentence_transformers import SentenceTransformer

# Load model and client once
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()

def search_products(intent_query, stage_bucket, budget=None, top_k=5):
    try:
        collection = client.get_collection("products")
    except Exception:
        # If collection doesn't exist, build it (failsafe)
        import sys
        sys.path.append("d:/MumzCompanion")
        from embeddings.build_index import build_index
        build_index()
        collection = client.get_collection("products")

    embedding = model.encode(intent_query if intent_query else "products").tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=20 # Fetch more to allow filtering
    )

    products = []
    if not results or not results["documents"]:
        return products

    for doc, dist in zip(results["documents"][0], results["distances"][0]):
        item = json.loads(doc)
        
        if stage_bucket not in item.get("stage_tags", []):
            continue
            
        if budget is not None and item.get("price_aed", 0) > budget:
            continue
            
        products.append({
            "item": item,
            "confidence": max(0.0, 1.0 - dist)
        })
        
        if len(products) == top_k:
            break

    return products