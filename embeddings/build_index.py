import json
import chromadb
from sentence_transformers import SentenceTransformer

def build_index():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.Client()
    # To avoid errors if running multiple times in same session:
    try:
        client.delete_collection("products")
    except:
        pass
    collection = client.create_collection("products")

    with open("d:/MumzCompanion/data/catalog.json", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        text = f"{item.get('name_en', '')} {item.get('name_ar', '')} {' '.join(item.get('tags', []))} {item.get('description_en', '')} {item.get('description_ar', '')}"
        embedding = model.encode(text).tolist()

        collection.add(
            ids=[item["id"]],
            embeddings=[embedding],
            documents=[json.dumps(item, ensure_ascii=False)]
        )

    print("Index built!")

if __name__ == "__main__":
    build_index()