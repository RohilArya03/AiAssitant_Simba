import requests
from app.config import OLLAMA_URL, MODEL_NAME

class ModelServingError(Exception):
    pass

def generate(messages: list[dict]) -> str:
    """
    The ONLY function in the codebase that knows Ollama exists.
    """
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False
    }
    response = _post_to_ollama(payload)
    return response["content"]


def generate_with_tools(messages: list[dict], tools: list[dict]) -> dict:
    """
    Like generate(), but includes tool definitions and returns the
    full response message (may contain a tool call or plain text).
    """
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "tools": tools,
        "stream": False
    }
    return _post_to_ollama(payload)


def _post_to_ollama(payload: dict) -> dict:
    """
    Shared request logic: POST to Ollama, handle errors, return the raw response's message dict.
    """
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise ModelServingError("Ollama is not running. Start it and try again.")
    except requests.exceptions.HTTPError as e:
        raise ModelServingError(f"Ollama request failed: {e}")

    data = response.json()
    return data["message"]