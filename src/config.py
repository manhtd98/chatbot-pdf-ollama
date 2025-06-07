PROMPT_TEMPLATE= """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context in a brief: {question}
"""


class CONFIG:
    # "mxbai-embed-large"
    EMBEDDING_MODEL = "nomic-embed-text"
    DATA_PDF_PATH = "data/"
    CHROMA_PATH = "chroma"
    OLLAMA_RESPONSE_MODEL = "qwen3:4b"
    TOP_K = 5
    
