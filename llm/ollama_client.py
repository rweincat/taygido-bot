import requests

from config import (
    OLLAMA_URL,
    OLLAMA_MODEL
)

# -----------------------------
# Ollama API 호출
# -----------------------------

def generate_llm_response(prompt: str) -> str:

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )

        data = response.json()

        return data.get("response", "").strip()

    except Exception as e:

        print(f"[OLLAMA ERROR] {e}")

        return ""