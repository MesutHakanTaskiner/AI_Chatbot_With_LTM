from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=API_KEY)


def embedding_creator(text: str) -> str:
    vector = embeddings.embed_query(text)

    return str(vector)
