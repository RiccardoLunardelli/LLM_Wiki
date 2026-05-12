import ollama


# LLM
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:8b"

# chiamata modello
def ollama_generate(prompt, json_mode=False):
    try:
        kwargs = {
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.0,
                "top_p": 0.9
            }
        }

        if json_mode:
            kwargs["format"] = "json"

        response = ollama.generate(**kwargs)

        return response.get("response", "").strip()

    except Exception as exc:
        raise RuntimeError(
            "Ollama non raggiungibile o modello non disponibile. "
            "Verifica che Ollama sia attivo e che llama3.1:8b sia installato."
        ) from exc
