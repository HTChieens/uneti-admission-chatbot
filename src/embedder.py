from langchain_openai import OpenAIEmbeddings

from .config import EMBEDDING_MODEL


model_embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
)
