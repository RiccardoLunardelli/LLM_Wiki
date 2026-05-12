import json
import re
from pathlib import Path
from datetime import datetime

from model_prompt import (
    INTENT_PROMPT,
    INGEST_PROMPT,
    QUERY_SELECT_PROMPT,
    QUERY_SYNTHESIS_PROMPT,
    LINT_PROMPT,
)
from ollama_client import ollama_generate


ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "raw"
WIKI_DIR = ROOT / "wiki"
AGENT_MD = ROOT / "agent.md"
INDEX_MD = ROOT / "index.md"
LOG_MD = ROOT / "log.md"


def now_date():
    return datetime.now().strftime("%Y-%m-%d")


def now_stamp():
    return datetime.now().strftime("%Y-%m-%d-%H%M%S")


def read_text(path):
    return path.read_text(encoding="utf-8")


def write_text(path, text):
    path.write_text(text, encoding="utf-8")


def append_text(path, text):
    with path.open("a", encoding="utf-8") as f:
        f.write(text)


def safe_slug(title):
    slug = title.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug, flags=re.UNICODE)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug[:80].strip("-") or "pagina"


def extract_json(text):
    if not isinstance(text, str):
        text = str(text)

    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError(f"Nessun JSON trovato nella risposta: {text!r}")

    return json.loads(match.group(0))


def classify_intent(user_input):
    prompt = INTENT_PROMPT.format(user_input=user_input)
    response = ollama_generate(prompt, json_mode=True)

    if not response.strip():
        raise RuntimeError(
            "Il modello ha restituito una risposta vuota durante la classificazione intent."
        )

    try:
        data = extract_json(response)
    except Exception as e:
        raise RuntimeError(
            f"JSON intent non valido.\nRisposta raw del modello:\n{response!r}"
        ) from e

    intent = data.get("intent")
    allowed = {"INGEST", "QUERY", "LINT", "HELP", "EXIT"}

    if intent not in allowed:
        raise RuntimeError(f"Intent non valido: {intent}")

    return intent


def resolve_ingest_source(user_input):
    payload = user_input.strip()

    if payload.lower().startswith("ingest "):
        payload = payload[7:].strip()

    candidate = ROOT / payload

    if payload.startswith("raw/") and candidate.exists() and candidate.is_file():
        if not candidate.resolve().is_relative_to(RAW_DIR.resolve()):
            raise RuntimeError("Il file ingest deve essere dentro raw/.")
        if candidate.suffix.lower() != ".md":
            raise RuntimeError("Sono ammessi solo file Markdown .md in raw/.")
        return candidate.relative_to(ROOT).as_posix(), read_text(candidate)

    stamp = now_stamp()
    filename = f"ingest-{stamp}.md"
    path = RAW_DIR / filename

    markdown = f"""# Ingest {stamp}

{payload}
"""

    write_text(path, markdown)

    return path.relative_to(ROOT).as_posix(), markdown


def load_existing_pages_for_ingest():
    chunks = []

    for path in sorted(WIKI_DIR.glob("*.md")):
        try:
            chunks.append(f"\n--- {path.relative_to(ROOT).as_posix()} ---\n{read_text(path)}")
        except Exception:
            continue

    if not chunks:
        return "Nessuna pagina esistente."

    return "\n".join(chunks)


def build_wiki_markdown(page, source_path):
    title = page.get("title", "Senza titolo")
    tags = page.get("tags", [])
    summary = page.get("summary", "")
    details = page.get("details", [])
    links = page.get("links", [])
    contradictions = page.get("contradictions", [])
    notes = page.get("notes", [])

    def list_or_empty(items):
        if not items:
            return "Nessuno."
        return "\n".join(f"- {item}" for item in items)

    tags_json = json.dumps(tags, ensure_ascii=False)
    source_json = json.dumps([source_path], ensure_ascii=False)

    return f"""---
title: "{title}"
date: "{now_date()}"
tags: {tags_json}
source: {source_json}
---

# {title}

## Sintesi

{summary}

## Dettagli

{list_or_empty(details)}

## Collegamenti

{list_or_empty(links)}

## Fonti

- {source_path}

## Contraddizioni

{list_or_empty(contradictions)}

## Note operative

{list_or_empty(notes)}
"""


def apply_ingest_result(result, source_path):
    pages = result.get("pages", [])

    if not isinstance(pages, list):
        raise RuntimeError("JSON ingest non valido: campo pages mancante o errato.")

    if not pages:
        raise RuntimeError(
            "L'ingest non ha prodotto nessuna pagina wiki. "
            "Il modello ha restituito pages vuoto."
        )

    for page in pages:
        title = page.get("title") or "Senza titolo"
        slug = page.get("slug") or safe_slug(title)

        markdown = build_wiki_markdown(page, source_path)
        path = WIKI_DIR / f"{safe_slug(slug)}.md"
        write_text(path, markdown.strip() + "\n")

    rebuild_index(result.get("index_entries", []))


def rebuild_index(new_entries):
    existing = {}

    if INDEX_MD.exists():
        text = read_text(INDEX_MD)
        for line in text.splitlines():
            match = re.match(r"- \[(.*?)\]\((wiki/.*?\.md)\) - (.*)", line)
            if match:
                existing[match.group(2)] = {
                    "title": match.group(1),
                    "path": match.group(2),
                    "summary": match.group(3),
                    "tags": [],
                }

    for entry in new_entries:
        path = entry.get("path")
        if not path:
            continue

        existing[path] = {
            "title": entry.get("title", path),
            "path": path,
            "summary": entry.get("summary", ""),
            "tags": entry.get("tags", []),
        }

    lines = ["# Index", ""]

    if not existing:
        lines.append("Nessuna pagina ancora presente.")
    else:
        for path in sorted(existing):
            entry = existing[path]
            tags = ", ".join(entry.get("tags", []))
            suffix = f" | tags: {tags}" if tags else ""
            lines.append(
                f"- [{entry['title']}]({entry['path']}) - {entry['summary']}{suffix}"
            )

    write_text(INDEX_MD, "\n".join(lines).strip() + "\n")


def handle_ingest(user_input):
    source_path, source_text = resolve_ingest_source(user_input)

    prompt = INGEST_PROMPT.format(
        date=now_date(),
        source_path=source_path,
        agent_rules=read_text(AGENT_MD),
        index=read_text(INDEX_MD),
        existing_pages=load_existing_pages_for_ingest(),
        source_text=source_text,
    )

    response = ollama_generate(prompt, json_mode=True)

    if not response.strip():
        raise RuntimeError("Il modello ha restituito una risposta vuota durante l'ingest.")

    try:
        result = extract_json(response)
    except Exception as e:
        raise RuntimeError(f"JSON ingest non valido:\n{response!r}") from e

    apply_ingest_result(result, source_path)

    append_text(
        LOG_MD,
        f"\n## [{now_date()}] INGEST | {source_path}\n",
    )

    return f"Ingest completato: {source_path}"


def normalize_wiki_path(path_text):
    path_text = path_text.strip()

    if path_text.startswith("/"):
        raise ValueError("Percorsi assoluti non ammessi.")

    path = ROOT / path_text

    if not path.resolve().is_relative_to(WIKI_DIR.resolve()):
        raise ValueError(f"Percorso fuori da wiki/: {path_text}")

    return path


def handle_query(user_input):
    question = user_input.strip()

    if question.lower().startswith("query "):
        question = question[6:].strip()

    select_prompt = QUERY_SELECT_PROMPT.format(
        question=question,
        index=read_text(INDEX_MD),
    )

    response = ollama_generate(select_prompt, json_mode=True)

    if not response.strip():
        raise RuntimeError("Il modello ha restituito una risposta vuota nella selezione pagine.")

    try:
        data = extract_json(response)
    except Exception as e:
        raise RuntimeError(f"JSON selezione pagine non valido:\n{response!r}") from e

    selected = data.get("pages", [])

    if not isinstance(selected, list):
        raise RuntimeError("Campo pages non valido nella selezione query.")

    chunks = []

    for item in selected:
        try:
            path = normalize_wiki_path(item)
            if path.exists():
                chunks.append(
                    f"\n--- {path.relative_to(ROOT).as_posix()} ---\n{read_text(path)}"
                )
        except Exception:
            continue

    if not chunks:
        return "Non ho trovato pagine wiki rilevanti."

    synthesis_prompt = QUERY_SYNTHESIS_PROMPT.format(
        question=question,
        pages_content="\n".join(chunks),
    )

    answer = ollama_generate(synthesis_prompt)
    return answer.strip()


def handle_lint():
    chunks = []

    for path in sorted(WIKI_DIR.glob("*.md")):
        chunks.append(f"\n--- {path.relative_to(ROOT).as_posix()} ---\n{read_text(path)}")

    if not chunks:
        return "Nessuna pagina wiki da analizzare."

    prompt = LINT_PROMPT.format(
        index=read_text(INDEX_MD),
        pages_content="\n".join(chunks),
    )

    report = ollama_generate(prompt)
    return report.strip()


def print_help():
    print(
        """
Comandi disponibili:

  ingest raw/nome-file.md
      Importa una fonte già presente in raw/.

  ingest testo libero
      Salva il testo in raw/ingest-YYYY-MM-DD-HHMMSS.md e lo importa.

  query domanda
      Interroga la wiki.

  lint
      Analizza la qualità della wiki senza modificare file.

  help
      Mostra questo aiuto.

  exit
      Esce dal programma.
""".strip()
    )


def ensure_structure():
    RAW_DIR.mkdir(exist_ok=True)
    WIKI_DIR.mkdir(exist_ok=True)

    if not INDEX_MD.exists():
        write_text(INDEX_MD, "# Index\n\nNessuna pagina ancora presente.\n")

    if not LOG_MD.exists():
        write_text(LOG_MD, "# Log\n")

    if not AGENT_MD.exists():
        raise RuntimeError("File agent.md mancante.")


def process_message(user_input):
    ensure_structure()

    user_input = user_input.strip()

    if not user_input:
        return {
            "ok": False,
            "answer": "Messaggio vuoto.",
        }

    intent = classify_intent(user_input)

    if intent == "EXIT":
        return {
            "ok": True,
            "answer": "Il comando EXIT non e' disponibile dal server web.",
        }

    if intent == "HELP":
        return {
            "ok": True,
            "answer": """
Comandi disponibili:

ingest raw/nome-file.md
ingest testo libero
query domanda
lint
help
""".strip(),
        }

    if intent == "LINT":
        return {
            "ok": True,
            "answer": handle_lint(),
        }

    if intent == "INGEST":
        return {
            "ok": True,
            "answer": handle_ingest(user_input),
        }

    if intent == "QUERY":
        return {
            "ok": True,
            "answer": handle_query(user_input),
        }

    return {
        "ok": False,
        "answer": f"Intent non gestito: {intent}",
    }


def main():
    ensure_structure()

    print("LLM Wiki locale")
    print("Scrivi 'help' per i comandi.")

    while True:
        try:
            user_input = input("\n> ").strip()

            if not user_input:
                continue

            intent = classify_intent(user_input)

            if intent == "EXIT":
                print("Uscita.")
                break

            if intent == "HELP":
                print_help()
                continue

            if intent == "LINT":
                print(handle_lint())
                continue

            if intent == "INGEST":
                print(handle_ingest(user_input))
                continue

            if intent == "QUERY":
                print(handle_query(user_input))
                continue

        except KeyboardInterrupt:
            print("\nUscita.")
            break
        except Exception as e:
            print(f"Errore: {e}")


if __name__ == "__main__":
    main()
