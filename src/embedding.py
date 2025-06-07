from langchain_community.embeddings.ollama import OllamaEmbeddings
from config import CONFIG

def get_embedding_function():
    embeddings = OllamaEmbeddings(model=CONFIG.EMBEDDING_MODEL)
    return embeddings