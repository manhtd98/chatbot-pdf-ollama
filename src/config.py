import os
PROMPT_TEMPLATE= """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context in a brief: {question}
"""


class CONFIG:
    # "mxbai-embed-large"
    EMBEDDING_MODEL = "nomic-embed-text"
    script_dir = os.path.dirname(os.path.abspath(__file__))

    DATA_PDF_PATH = script_dir + "/data/"
    CHROMA_PATH = script_dir + "/chroma"
    OLLAMA_RESPONSE_MODEL = "qwen3:4b"
    TOP_K = 5
    
