from django.conf import settings
from langchain_community.vectorstores import FAISS
from langchain_ollama.embeddings import OllamaEmbeddings


# def load_vectorstore():
#     embeddings = OllamaEmbeddings(model=settings.EMBEDDINGS_MODEL)
#     vector_store = FAISS('faiss_index', embeddings)

#     return vector_store


# def create_post(query: str, personality: str, username: str) -> str:
#     """Creates a post with a provided personality and username"""
#     vs = load_vectorstore()

#     previous_posts = vs.similarity_search(filter={'username': username})

#     if len(previous_posts) > 0:
#         return previous_posts
