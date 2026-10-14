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

def build_vector_store(chunks: list[str], store_filename: str) -> list[tuple[str, list[float]]]:
    """
    Embeds each chunk and returns a list of (text, embedding) pairs.
    """
    filepath = os.path.join(VECTOR_STORE_DIR, store_filename)

    store = []
    existing_store = load_vector_store(filepath) if os.path.exists(filepath) else []
    existing_store_dict = {text: embedding for text, embedding in existing_store}  # For quick lookup
    for chunk in chunks:
        if chunk in existing_store_dict:
            embedded_chunk = existing_store_dict[chunk]  # Reuse existing embedding
        else:
            embedded_chunk = embed_text(chunk)
        store.append((chunk, embedded_chunk))
    save_vector_store(store, filepath)  # Save the updated store to disk
    return store

