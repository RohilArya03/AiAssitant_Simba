from app.rag.chunker import split_into_paragraphs, pack_paragraphs
from app.rag.search import search
from app.rag.vector_store import build_vector_store

raw_notes = """Dentist appointment is Tuesday at 2pm with Dr. Martinez downtown.

Need to call the contractor about the fence repair estimate.

Rent is due on the 1st of the month, pay via e-transfer.

Grocery list: milk, eggs, bread, coffee."""

paragraphs = split_into_paragraphs(raw_notes)
chunks = pack_paragraphs(paragraphs, max_chunk_size=80)
store = build_vector_store(chunks)

print(f"Store has {len(store)} chunks:")
for text, _ in store:
    print(f"  - {text}")

print()
results = search("when do I need to pay rent?", store, top_k=2)
print("Top matches for 'when do I need to pay rent?':")
for r in results:
    print(f"  - {r}")