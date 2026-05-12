import ollama
import json


# LLM
MODEL = "llama3.1:8b" #"gpt-oss:20b"

# chiamata modello
def ollama_generate(prompt, json_mode=False):
    try:
        kwargs = {
            "model": MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "options": {
                "temperature": 0.0
            }
        }

        if json_mode:
            kwargs["format"] = "json"

        response = ollama.chat(**kwargs)

        content = response["message"]["content"].strip()

        print("RESPONSE RAW:", repr(response))
        print("RESPONSE TEXT:", repr(content))

        if not content:
            raise RuntimeError("Il modello ha restituito una risposta vuota.")

        if json_mode:
            json.loads(content)

        return content

    except Exception as exc:
        raise RuntimeError(
            f"Ollama non raggiungibile o modello non disponibile. "
            f"Verifica che Ollama sia attivo e che {MODEL} sia installato. "
            f"Errore originale: {exc}"
        ) from exc
