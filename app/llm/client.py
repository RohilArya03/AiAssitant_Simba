import requests
from app.config import OLLAMA_URL, MODEL_NAME

class ModelServingError(Exception):
    pass

def generate(messages: list[dict]) -> str:
    """
    The ONLY function in the codebase that knows Ollama exists.
    """
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "messages": messages,
            "stream": False
        })
        response.raise_for_status()
#This is Ollama specific error. If we ever upgrade need to swap this out for vLLM specific
    except requests.exceptions.ConnectionError: 
        raise ModelServingError(
            "Ollama is not running. Start it and try again."
        )
    
    except requests.exceptions.HTTPError as e:
        raise ModelServingError(
            f"Ollama request failed: {e}"
        )

    data = response.json()
    #For debugging purposes, you can uncomment the following line to see the full response from Ollama
    # print(f"DEBUG: Ollama response: {data}")
    return data["message"]["content"]