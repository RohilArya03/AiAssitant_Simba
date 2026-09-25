from app.rag.ingest import read_notes_file
from app.rag.chunker import split_into_paragraphs, pack_paragraphs
from app.rag.vector_store import build_vector_store
from app.rag.search import search
from app.config import NOTE_STORE_PATH

raw_text = read_notes_file("data/notes/my_notes.txt")
paragraphs = split_into_paragraphs(raw_text)
chunks = pack_paragraphs(paragraphs, max_chunk_size=100)
store = build_vector_store(chunks, NOTE_STORE_PATH)

results = search("what is my grocery list?", store, top_k=2)
for r in results:
    print(r)