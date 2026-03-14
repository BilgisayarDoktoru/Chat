from flask import Flask, request, jsonify, render_template
from datetime import datetime
import json, os

app = Flask(__name__)
MESSAGES_FILE = "messages.json"

def load():
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE) as f:
        return json.load(f)

def save(msgs):
    with open(MESSAGES_FILE, "w") as f:
        json.dump(msgs[-100:], f)  # Son 100 mesajı sakla

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    if not data or not data.get("text", "").strip():
        return jsonify({"ok": False, "error": "Boş mesaj"}), 400
    msgs = load()
    msgs.append({
        "user": data.get("user", "Anonim")[:20],
        "text": data.get("text", "")[:500],
        "time": datetime.now().strftime("%H:%M")
    })
    save(msgs)
    return jsonify({"ok": True})

@app.route("/messages")
def messages():
    return jsonify(load())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
