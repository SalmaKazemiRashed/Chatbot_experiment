import streamlit as st
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# --------------------------
# Define LangGraph state
# --------------------------
class RAGState(TypedDict):
    question: str
    docs: List[Document]
    context: str
    answer: str

# --------------------------
# Node 1: Load PDF
# --------------------------
def load_pdf(state: RAGState):
    loader = PyPDFLoader("1._Intro_to_AI_-_Course_notes.pdf")
    docs = loader.load()
    for d in docs:
        d.page_content = d.page_content.replace("\x00", "").replace("\n", " ").strip()
    return {"docs": docs}

# --------------------------
# Node 2: Split documents
# --------------------------
def split_docs(state: RAGState):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(state["docs"])
    return {"docs": chunks}

# --------------------------
# Node 3: Retrieve relevant context
# --------------------------
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma(
    persist_directory="intro-to-ai",
    embedding_function=embeddings
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

def retrieve(state: RAGState):
    docs = retriever.invoke(state["question"])
    context = "\n\n".join(d.page_content for d in docs)
    return {"context": context}

# --------------------------
# Node 4: Generate answer
# --------------------------
prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant.
Use the context below to answer the question.

Context:
{context}

Question:
{question}
""")
llm = ChatOllama(model="llama3", temperature=0)

def generate_answer(state: RAGState):
    messages = prompt.invoke({
        "context": state["context"],
        "question": state["question"]
    })
    response = llm.invoke(messages)
    return {"answer": response.content}

# --------------------------
# Build the LangGraph
# --------------------------
graph = StateGraph(RAGState)
graph.add_node("load_pdf", load_pdf)
graph.add_node("split_docs", split_docs)
graph.add_node("retrieve", retrieve)
graph.add_node("generate_answer", generate_answer)
graph.set_entry_point("load_pdf")
graph.add_edge("load_pdf", "split_docs")
graph.add_edge("split_docs", "retrieve")
graph.add_edge("retrieve", "generate_answer")
graph.add_edge("generate_answer", END)

app_graph = graph.compile()

# --------------------------
# Streamlit UI
# --------------------------
st.set_page_config(page_title="RAG QA App", layout="wide")
st.title("📄 PDF Question Answering (RAG + LangGraph)")

question = st.text_input("Ask a question about the PDF:")

if st.button("Get Answer") and question:
    with st.spinner("Thinking..."):
        result = app_graph.invoke({"question": question})
        answer = result.get("answer", "No answer found.")
    st.subheader("Answer:")
    st.write(answer)