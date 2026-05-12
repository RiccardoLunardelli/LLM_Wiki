# 10.0.20.68

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
from threading import Lock

from agent import process_message


HOST = "0.0.0.0"
PORT = 8000

agent_lock = Lock()


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
        const response = await fetch("/api/ask", {
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


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path

        if path != "/":
            self.send_error(404)
            return

        body = HTML.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        path = urlparse(self.path).path

        if path != "/api/ask":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(length)
            data = json.loads(raw_body.decode("utf-8"))

            question = data.get("question", "")

            with agent_lock:
                result = process_message(question)

            self.send_json(200, result)

        except Exception as exc:
            self.send_json(500, {
                "ok": False,
                "error": str(exc)
            })


def main():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Server attivo su http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
