import pytest
from unittest.mock import patch
from app.llm.client import generate, ModelServingError
import requests

def test_generate_raises_when_ollama_down():
    with patch("app.llm.client.requests.post", side_effect=requests.exceptions.ConnectionError):
        with pytest.raises(ModelServingError):
            generate([{"role": "user", "content": "hi"}])