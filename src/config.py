from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = BASE_DIR / "data" / "documents"
VECTORSTORE_PATH = BASE_DIR / "vectorstore_cache"

CHAT_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"

RETRIEVER_K = 8
RETRIEVER_FETCH_K = 30
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200
