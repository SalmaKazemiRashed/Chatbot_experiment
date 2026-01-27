# Chatbot_experiment


## LLM chatbot + RAG

langchain

langchain-ollama 

faiss/Chroma

Ollama (llama3, nomic-embed-text)

Integrated with StreamLit UI


!()[./RAG_chatbot/static/LLM_chatbot.png]

```plaintext
├── RAG_chatbot/
|   ├── LLM_chatbot.py
|   ├── app.py
│   ├── LLM_langgraph_app.py
```

The steps were 
A. install packages

``` bash
!pip install -U langchain langchain-ollama langchain-community faiss-cpu
```

B. Load and split documents 

C. Embeddings

D. Vectorstore

E. LLM

F. Prompt

G. RAG chain

H. Invoke



!()[./RAG_chatbot/static/LLM_chatbot_langgraph.png]

## LLM chatbot + RAG + langraph

Define LangGraph state

Node A: Load PDF

Node B: Split documents

Node C: Retrieve relevant context

Node D: Generate answer

Build the LangGraph

Streamlit UI





* This is a simple chatbot project Using FLASK backend ready for depolyment (Dockerized)

* Integrated with Neo4j for Graph RAG

* Use of LLM API


First, I made project structure as follows:
```plaintext
chatbot_experiment/
├── app/
|   ├── __init__.py
|   ├── config.py
│   ├── neo4j_client.py
│   ├── llm_client.py
|   ├── routes.py
│   └── utils.py
├── main.py   
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

