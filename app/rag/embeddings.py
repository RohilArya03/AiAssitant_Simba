from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL_NAME

_model = None

def embed_text(text: str) -> list[float]:
    """
    The ONLY function that knows which embedding model/library is being used.
    """
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _model.encode(text).tolist()