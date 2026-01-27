from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import os

PERSIST_DIR = "intro-to-ai"

def build_vectorstore():
    if os.path.exists(PERSIST_DIR):
        return

    loader = PyPDFLoader("1._Intro_to_AI_-_Course_notes.pdf")
    docs = loader.load()

    for d in docs:
        d.page_content = (
            d.page_content.replace("\x00", "")
            .replace("\n", " ")
            .strip()
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=150
    )
    chunks = splitter.split_documents(docs)

    # remove junk chunks
    chunks = [
        c for c in chunks
    ]

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )

build_vectorstore()

from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")

vectorstore = Chroma(
    persist_directory="intro-to-ai",
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 6}
)

prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant.
Answer the question using only the context below.
If the answer is not in the context, say you don’t know.

Context:
{context}

Question:
{question}
""")

llm = ChatOllama(model="llama3", temperature=1)


def ask_chatbot(question: str) -> str:
    docs = retriever.invoke(question)

    context = "\n\n".join(
        d.page_content for d in docs
    )

    chain = (
        {
            "context": lambda _: context,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
    )

    return chain.invoke(question).content
