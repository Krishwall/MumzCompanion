# MumzCompanion 🤰

MumzCompanion is a timeline-aware multilingual pediatric product discovery agent. 

A mom at week 32 and a mom with a 6-month-old have almost zero product overlap — yet they typically get identical recommendations on most e-commerce platforms. MumzCompanion solves this by making her stage the primary context for all discovery, so the catalog becomes a living guide that evolves with her.

## Setup Instructions (Under 5 minutes)

1. Create a virtual environment: `python -m venv venv` and activate it.
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your LLM API keys:
   ```env
   OPENAI_API_KEY=your_key_here
   # OPENAI_BASE_URL=https://api.groq.com/openai/v1  # if using Groq or OpenRouter
   # LLM_MODEL=llama3-8b-8192
   ```
4. Build the embedding index: `python embeddings/build_index.py`
5. Run the Streamlit UI: `streamlit run app.py`

## Architecture

- **UI**: Streamlit (Light Theme, RTL support for Arabic).
- **Orchestration Loop**: `agent.py` processes language detection, stage calculation, intent extraction, RAG, and insight generation.
- **Tools**: Langdetect, OpenAI-compatible APIs (OpenRouter, Groq).
- **RAG**: ChromaDB locally caching SentenceTransformers (`all-MiniLM-L6-v2`).

## Tradeoffs

The biggest risk in this system is hallucinating product details — a mom acting on a wrong price or wrong age-range recommendation is a real harm. I mitigated this by grounding every product in the validated catalog (no product is generated, only retrieved), and the Pydantic schema ensures any malformed output fails explicitly rather than silently. The one thing I would add with more time is a re-ranker that checks the LLM's relevance_reason against the actual product tags to catch confabulation.

I used ChromaDB over Pinecone because it's fully local and free — the tradeoff is no persistence across deploys, which I'd fix in production by persisting the collection to disk or moving to a managed vector store.

## Tooling Recommendation
- **LLM**: Meta Llama 3 70B (via Groq/OpenRouter) — handles Arabic natively and quickly.
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` — fully local, zero cost.
- **Schemas**: Pydantic v2.

## Evals

Run `python evals/run_evals.py` to execute our 12 comprehensive test cases, validating safe medical refusal, bilingual outputs, and temporal accuracy.