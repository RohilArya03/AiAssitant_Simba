from app.rag.chunker import pack_paragraphs ,split_into_paragraphs

paragraphs = [
    "This is the first paragraph about a dentist appointment on Tuesday.",
    "This is a second paragraph about calling the contractor for repairs.",
    "A third short paragraph.",
    "This fourth paragraph is intentionally very long, much longer than one hundred characters, to prove that pack_paragraphs currently has no way to split a single paragraph that exceeds max_chunk_size on its own, which is exactly the gap we need to fix next with sentence-level fallback splitting."
]

result = pack_paragraphs(paragraphs, max_chunk_size=100)
for i, chunk in enumerate(result):
    print(f"Chunk {i}: length {len(chunk)} (limit was 100)")


raw_notes = """Dentist appt Tuesday 2pm.


Call contractor about the fence.

Pay rent by the 1st."""

paragraphs = split_into_paragraphs(raw_notes)
print(paragraphs)

chunks = pack_paragraphs(paragraphs, max_chunk_size=100)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i}: length {len(chunk)} (limit was 100)")