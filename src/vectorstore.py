from langchain_community.vectorstores.utils import DistanceStrategy

from langchain_community.vectorstores import FAISS

from .config import VECTORSTORE_PATH
from .embedder import model_embeddings
from .loader import clean_and_merge_docs, load_pdf
from .splitter import split


def build_vectorstore(docs):
    db = FAISS.from_documents(
        documents=docs,
        embedding=model_embeddings,
        distance_strategy=DistanceStrategy.COSINE
    )
    return db


def load_vectorstore():
    if VECTORSTORE_PATH.exists():
        print("Loading vectorstore from cache...")
        db = FAISS.load_local(
            str(VECTORSTORE_PATH),
            model_embeddings,
            allow_dangerous_deserialization=True
        )
    else:
        print("Building vectorstore lần đầu...")
        docs = load_pdf()
        clean_docs = clean_and_merge_docs(docs)
        splits = split(clean_docs)
        db = build_vectorstore(splits)
        db.save_local(str(VECTORSTORE_PATH))
        print(f"Đã lưu vectorstore vào '{VECTORSTORE_PATH}'")
    return db
