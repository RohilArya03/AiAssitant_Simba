from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL_NAME

_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def embed_text(text: str) -> list[float]:
    """
    The ONLY function that knows which embedding model/library is being used.
    """
    return _model.encode(text).tolist()