import pickle
import faiss
import openai
from sentence_transformers import SentenceTransformer

openai.api_key = "sk-..."  # Use key

def load_index():
    with open("index.pkl", "rb") as f:
        index, docs = pickle.load(f)
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return index, docs, embedder

def generate_answer(query, index, docs, embedder):
    q_vec = embedder.encode([query])
    D, I = index.search(q_vec, k=3)
    context = "\n".join([docs[i] for i in I[0]])

    prompt = f"Use this context to answer:\n{context}\n\nQuestion: {query}"
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return res['choices'][0]['message']['content']