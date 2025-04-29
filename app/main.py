from flask import Flask, request, jsonify

from rag import load_index, generate_answer

app = Flask(__name__)
index, docs, embedder = load_index()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    answer = generate_answer(query, index, docs, embedder)
    return jsonify({"answer": answer})