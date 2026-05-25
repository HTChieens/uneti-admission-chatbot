import os
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()
model_embeddings = OpenAIEmbeddings(
    model = "text-embedding-3-small",
    api_key= os.getenv("OPENAI_API_KEY")
)
