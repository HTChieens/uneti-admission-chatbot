from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from .embedder import model_embeddings
import os
from src.loader import load_pdf,clean_and_merge_docs
from src.splitter import split
from pprint import pprint
VECTORSTORE_PATH = "vectorstore_cache"
def build_vectorstore(docs):
    db = FAISS.from_documents(
        documents=docs,
        embedding=model_embeddings,
        distance_strategy=DistanceStrategy.COSINE
    )
    return db
def load_vectorstore():
    if os.path.exists(VECTORSTORE_PATH):
        print("Loading vectorstore from cache...")
        db = FAISS.load_local(VECTORSTORE_PATH, model_embeddings, allow_dangerous_deserialization=True)
    else:
        print("Building vectorstore lần đầu...")
        docs = load_pdf()
        clean_docs =clean_and_merge_docs(docs)
        splits = split(clean_docs)
        pprint(splits)
        db = build_vectorstore(splits)
        db.save_local(VECTORSTORE_PATH)
        print(f"Đã lưu vectorstore vào '{VECTORSTORE_PATH}'")
    return db

