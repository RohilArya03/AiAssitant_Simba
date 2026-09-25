from app.rag.embeddings import embed_text
from app.config import VECTOR_STORE_DIR

import os
import pickle

def save_vector_store(store: list[tuple[str, list[float]]], filepath: str) -> None:
    """
    Save the vector store to disk using pickle.
    """
    with open(filepath, 'wb') as f:
        pickle.dump(store, f)

def load_vector_store(filepath: str) -> list[tuple[str, list[float]]]:
    """
    Load the vector store from disk and return the stored embeddings.
    """
    with open(filepath, 'rb') as f:
        return pickle.load(f)

def find_new_chunks(chunks: list[str], existing_store: list[tuple[str, list[float]]]) -> list[str]:
    """
    Given fresh chunks and an already-loaded store, returns only the chunks
    that aren't already present — the ones that actually need embedding.
    """
    existing_texts = {text for text, _ in existing_store}  # build the fast-lookup set
    
    new_chunks = []
    for chunk in chunks:
        if chunk not in existing_texts:
            new_chunks.append(chunk)
    
    return new_chunks

def build_vector_store(chunks: list[str], store_filename: str) -> list[tuple[str, list[float]]]:
    """
    Embeds each chunk and returns a list of (text, embedding) pairs.
    """
    filepath = os.path.join(VECTOR_STORE_DIR, store_filename)

    store = []
    existing_store = load_vector_store(filepath) if os.path.exists(filepath) else []
    chunks = find_new_chunks(chunks, existing_store)  # Filter out already embedded chunks
    for chunk in chunks:
        embedded_chunk = embed_text(chunk)
        store.append((chunk, embedded_chunk))
    full_store = existing_store + store  # Combine existing and new embeddings
    save_vector_store(full_store, filepath)  # Save the updated store to disk
    return full_store

