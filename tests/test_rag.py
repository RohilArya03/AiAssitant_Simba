from unittest.mock import patch
from app.rag.vector_store import build_vector_store

def test_build_vector_store_drops_removed_chunks_and_reuses_embeddings(tmp_path):
    with patch("app.rag.vector_store.VECTOR_STORE_DIR", str(tmp_path)), \
         patch("app.rag.vector_store.embed_text", return_value=[0.1, 0.2]) as fake_embed:
        build_vector_store(["a", "b"], "store.pkl")
        assert fake_embed.call_count == 2

        store = build_vector_store(["a", "c"], "store.pkl")

    assert [text for text, _ in store] == ["a", "c"]   # "b" is gone
    assert fake_embed.call_count == 3                   # only "c" was newly embedded