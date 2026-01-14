from settings import EMBEDDINGS_MODEL

from langchain_community.vectorstores import FAISS
from langchain_ollama.embeddings import OllamaEmbeddings


class VectorStore:
    # Currently unused
    def __init__(self):
        self.vs = ''
        self.embeddings = OllamaEmbeddings(model=EMBEDDINGS_MODEL)

    def _build_vector_store(self):
        self.vs = FAISS.from_documents('', embedding=self.embeddings)
        pass
