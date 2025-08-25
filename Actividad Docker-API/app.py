import os
import json
import time
from pathlib import Path
from flask import Flask, request, jsonify

app = Flask(__name__)

# Ruta del archivo donde se guardan las notas (en volumen)
NOTES_FILE = os.getenv("NOTES_FILE", "/data/notes.txt")
Path(os.path.dirname(NOTES_FILE) or ".").mkdir(parents=True, exist_ok=True)
Path(NOTES_FILE).touch(exist_ok=True)

def _append_note(text: str):
    text = (text or "").strip()
    if not text:
        raise ValueError("La nota no puede estar vacía.")
    entry = {"ts": int(time.time()), "note": text}
    # Guardamos como JSONL para que sea fácil de leer/parsear
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry

def _read_notes():
    notes = []
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                notes.append(json.loads(line))
            except json.JSONDecodeError:
                # Si hubiera una línea corrupta, la ignoramos
                continue
    return notes

@app.get("/")
def root():
    title = os.getenv("API_TITLE", "API de notas")
    return jsonify(status="ok", message=f"{title} activa"), 200

# Opción 1: vía path param, p.ej. /add/Hola%20mundo
@app.post("/add/<path:note>")
def add_with_path(note):
    try:
        entry = _append_note(note)
        return jsonify(ok=True, saved=entry), 201
    except ValueError as e:
        return jsonify(ok=False, error=str(e)), 400

# Opción 2: vía body (JSON o form). Útil si la nota es larga.
@app.post("/add")
def add_with_body():
    # Prioridad: JSON -> form -> text/plain
    note = None
    if request.is_json:
        data = request.get_json(silent=True) or {}
        note = data.get("note")
    if note is None:
        note = request.form.get("note")
    if note is None:
        note = request.get_data(as_text=True)

    try:
        entry = _append_note(note)
        return jsonify(ok=True, saved=entry), 201
    except ValueError as e:
        return jsonify(ok=False, error=str(e)), 400

@app.get("/list")
def list_notes():
    notes = _read_notes()
    # Ordenadas por fecha ascendente (primero = más antiguo)
    notes.sort(key=lambda x: x.get("ts", 0))
    return jsonify(count=len(notes), results=notes), 200

if __name__ == "__main__":
    # Para correr local: python app.py
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
