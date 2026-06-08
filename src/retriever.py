import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

PERSIST_DIR = "embeddings"

def get_retriever():

    if not os.path.exists(PERSIST_DIR):
        from src.ingest import ingest_documents
        ingest_documents()

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )

    print("Vector DB document count:", vectorstore._collection.count())

    return vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 6, "fetch_k": 12}
    )