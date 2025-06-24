from flask import Blueprint, request, jsonify
from .neo4j_client import Neo4jClient
from .llm_chain import generate_response

routes = Blueprint('routes', __name__)
neo4j_client = Neo4jClient()

@routes.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "No message provided."}), 400

    context = neo4j_client.get_relevant_context(user_input)
    answer = generate_response(user_input, context)
    return jsonify({"response": answer})
