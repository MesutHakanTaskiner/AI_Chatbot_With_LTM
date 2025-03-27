from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from sklearn.metrics.pairwise import cosine_similarity
from utils.config import API_KEY

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=API_KEY)


def get_embedding(text: str) -> str:
    vector = embeddings.embed_query(text)

    return str(vector)


def compare_embeddings(embed1: str, embed2: str) -> float:
    similarity_score = cosine_similarity(embed1, embed2)[0][0]
    print("similarity", similarity_score)

    if similarity_score > 0.7:
        return False
    else:
        return True