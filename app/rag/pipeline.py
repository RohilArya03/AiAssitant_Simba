from app.rag.search import search
from app.rag.rerank import rerank
from app.rag.chunker import pack_paragraphs, split_into_paragraphs
from app.rag.ingest import read_notes_file
from app.rag.vector_store import build_vector_store
from app.config import NOTE_STORE_PATH, NOTES_FILE_PATH, CHUNK_SIZE


def run_rag_pipeline(question: str) -> list[str]:
    """
    Given a question, runs the full RAG pipeline end to end:
    read notes → chunk → embed/store → search → rerank → return best chunks.
    """
    raw_text = read_notes_file(NOTES_FILE_PATH)
    paragraphs = split_into_paragraphs(raw_text)
    chunks = pack_paragraphs(paragraphs, max_chunk_size=CHUNK_SIZE)
    store = build_vector_store(chunks, NOTE_STORE_PATH)
    top_results = search(question, store, top_k=5)
    final_results = rerank(question, top_results)
    return final_results