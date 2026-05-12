import threading

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn

from agent import process_message


HOST = "0.0.0.0"
PORT = 8000

agent_lock = threading.Lock()


HTML = """
<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <title>Personal Bot</title>
  <style>
    body {
      font-family: system-ui, sans-serif;
      max-width: 900px;
      margin: 40px auto;
      padding: 0 16px;
      background: #f6f6f6;
    }

    textarea {
      width: 100%;
      min-height: 120px;
      font-size: 16px;
      padding: 12px;
      box-sizing: border-box;
    }

    button {
      margin-top: 12px;
      padding: 10px 16px;
      font-size: 16px;
      cursor: pointer;
    }

    pre {
      white-space: pre-wrap;
      background: white;
      padding: 16px;
      border: 1px solid #ddd;
      min-height: 120px;
    }
  </style>
</head>
<body>
  <h1>Personal Bot</h1>

  <textarea id="question" placeholder="Scrivi una domanda..."></textarea>
  <br>
  <button onclick="ask()">Invia</button>

  <h2>Risposta</h2>
  <pre id="answer"></pre>

  <script>
    async function ask() {
      const question = document.getElementById("question").value;
      const answerBox = document.getElementById("answer");

      answerBox.textContent = "Elaborazione...";

      try {
        const response = await fetch("/api/prompt", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ question })
        });

        const data = await response.json();

        if (!response.ok || !data.ok) {
          answerBox.textContent = data.error || data.answer || "Errore.";
          return;
        }

        answerBox.textContent = data.answer;
      } catch (err) {
        answerBox.textContent = "Errore di rete: " + err.message;
      }
    }
  </script>
</body>
</html>
"""


class AskRequest(BaseModel):
    question: str


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():
    return HTML


@app.post("/api/prompt")
def ask(payload: AskRequest):
    try:
        with agent_lock:
            result = process_message(payload.question)
        return JSONResponse(status_code=200, content=result)
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "ok": False,
                "error": str(exc),
            },
        )


def main():

    print(f"Server attivo su http://{HOST}:{PORT}")
    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()
