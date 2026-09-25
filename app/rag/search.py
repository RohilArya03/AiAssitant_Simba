from app.rag.embeddings import embed_text
import numpy as np

def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    Calculate the cosine similarity between two vectors.
    Return 0 when either vector has zero magnitude.
    """
    a = np.array(vec_a)
    b = np.array(vec_b)
    dot_product = np.dot(a, b)
    magnitude_a = np.linalg.norm(a)
    magnitude_b = np.linalg.norm(b)
    if magnitude_a == 0 or magnitude_b == 0:
        return 0
    return dot_product / (magnitude_a * magnitude_b)


def search(question: str, store: list[tuple[str, list[float]]], top_k: int = 3) -> list[str]:
    """
    Embeds the question, compares it against every chunk in the store,
    and returns the top_k most similar chunks' text.
    """
    # 1. Embed the question using embed_text
    question_embedding = embed_text(question)
    # 2. Calculate cosine similarity between the question embedding and each chunk's embedding
    similarities = []
    for chunk, embedding in store:
        similarity = cosine_similarity(question_embedding, embedding)
        similarities.append((chunk, similarity))
    # 3. Sort the chunks by similarity in descending order
    similarities.sort(key=lambda x: x[1], reverse=True)
    # 4. Return the top_k most similar chunks' text
    return [chunk for chunk, _ in similarities[:top_k]]