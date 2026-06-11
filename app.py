import os
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

def headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

@app.route("/")
def index():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return "<h2>❌ Faltan SUPABASE_URL y SUPABASE_KEY en las variables de entorno de Render.</h2>", 500

    r = requests.get(f"{SUPABASE_URL}/rest/v1/items?select=*", headers=headers())

    if not r.ok:
        return f"<h2>❌ Error de Supabase ({r.status_code}):</h2><pre>{r.text}</pre>", 500

    items = r.json() if r.text else []
    return render_template("index.html", items=items)

@app.route("/add", methods=["POST"])
def add():
    nombre = request.form.get("nombre")
    if nombre:
        requests.post(f"{SUPABASE_URL}/rest/v1/items", json={"nombre": nombre}, headers=headers())
    return redirect(url_for("index"))

@app.route("/delete/<int:item_id>")
def delete(item_id):
    requests.delete(f"{SUPABASE_URL}/rest/v1/items?id=eq.{item_id}", headers=headers())
    return redirect(url_for("index"))

@app.route("/edit/<int:item_id>", methods=["POST"])
def edit(item_id):
    nuevo_nombre = request.form.get("nombre")
    if nuevo_nombre:
        requests.patch(f"{SUPABASE_URL}/rest/v1/items?id=eq.{item_id}", json={"nombre": nuevo_nombre}, headers=headers())
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
