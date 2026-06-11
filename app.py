import os
from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client

app = Flask(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def index():
    response = supabase.table("items").select("*").execute()
    items = response.data
    return render_template("index.html", items=items)

@app.route("/add", methods=["POST"])
def add():
    nombre = request.form.get("nombre")
    if nombre:
        supabase.table("items").insert({"nombre": nombre}).execute()
    return redirect(url_for("index"))

@app.route("/delete/<int:item_id>")
def delete(item_id):
    supabase.table("items").delete().eq("id", item_id).execute()
    return redirect(url_for("index"))

@app.route("/edit/<int:item_id>", methods=["POST"])
def edit(item_id):
    nuevo_nombre = request.form.get("nombre")
    if nuevo_nombre:
        supabase.table("items").update({"nombre": nuevo_nombre}).eq("id", item_id).execute()
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
