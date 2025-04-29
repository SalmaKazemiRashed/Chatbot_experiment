import pickle
import faiss
from sentence_transformers import SentenceTransformer

docs = [
    "Flask is a lightweight WSGI web application framework.",
    "FAISS is a library for efficient similarity search.",
    "OpenAI provides APIs for large language models."
]

model = SentenceTransformer("all-MiniLM-L6-v2")
vectors = model.encode(docs)

index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

with open("index.pkl", "wb") as f:
    pickle.dump((index, docs), f)