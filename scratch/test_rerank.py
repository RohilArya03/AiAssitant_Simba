from app.rag.chunker import split_into_paragraphs, pack_paragraphs
from app.rag.embeddings import embed_text
from app.rag.vector_store import build_vector_store
from app.rag.search import search
from app.rag.rerank import rerank

raw_notes = """Dentist appointment is Tuesday at 2pm with Dr. Martinez downtown.

Need to call the contractor about the fence repair estimate.

Rent is due on the 1st of the month, pay via e-transfer.

Grocery list: milk, eggs, bread, coffee."""

paragraphs = split_into_paragraphs(raw_notes)
chunks = pack_paragraphs(paragraphs, max_chunk_size=80)
store = build_vector_store(chunks)

question = "when do I need to pay rent?"
top_results = search(question, store, top_k=3)

print("Before rerank:")
for r in top_results:
    print(f"  - {r}")

reranked = rerank(question, top_results)

print("\nAfter rerank:")
for r in reranked:
    print(f"  - {r}")