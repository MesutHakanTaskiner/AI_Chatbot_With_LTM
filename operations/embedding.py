from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=API_KEY)


def get_embedding(text: str) -> str:
    vector = embeddings.embed_query(text)

    return str(vector)


# Cosine similarity between two embeddings
def cosine_similarity(embedding1: str, embedding2: str) -> float:
    return embeddings.cosine_similarity(embedding1, embedding2)