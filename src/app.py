from rag_query import query_rag
from embedding import get_embedding_function
from load_docs import document_load_pdf
from langchain_community.vectorstores import Chroma
from langchain_community.llms.ollama import Ollama
from config import CONFIG
import streamlit as st
import os


embedding_function = get_embedding_function()
CHROME_DB = Chroma(persist_directory=CONFIG.CHROMA_PATH, embedding_function=embedding_function)
OLLAMA_MODEL = Ollama(model=CONFIG.OLLAMA_RESPONSE_MODEL)
def main():
    st.set_page_config(page_title="Chat PDF Ollama ChromaDB", layout="wide")

    # Sidebar
    with st.sidebar:
        st.title("ChatBot")
        st.info("Welcome to Chat PDF Ollama ChromaDB! Upload PDFs, ask questions, and explore document content interactively.")

        # Options
        st.subheader("Options")
        enable_summarization = st.checkbox("Enable Summarization", help="Get concise summaries of responses.")
        enable_highlighting = st.checkbox("Enable Text Highlighting", help="Highlight relevant parts of the document in the response.")

    # Main layout
    st.title("Chat with Your PDF")
    st.write("Upload a PDF file and interact with its content using AI-powered responses.")

    # File upload section
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"], help="Upload your PDF file here to begin.")

    if uploaded_file is not None:
        file_name = os.path.join(CONFIG.DATA_PDF_PATH, uploaded_file.name)
        with open(file_name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        document_load_pdf(CHROME_DB, file_name)
        # Placeholder for loading the file content
        st.success("Loading file content successfully!")
        # Option to download the uploaded file
        with open(file_name, "rb") as f:
            st.download_button(label="Download uploaded file",
                               data=f,
                               file_name=uploaded_file.name,
                               mime="application/pdf")

    # Chat section
    st.divider()
    st.header("Chat Section")
    st.header(f"Total document: {len(CHROME_DB)}")
    st.write("Enter your question below to chat with the content of your uploaded PDF.")

    # Initialize chat messages
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "Welcome, get ready to be mind blown by AI!"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User-provided prompt
    input_txt = st.chat_input("Ask your question here...")

    if input_txt:
        st.session_state.messages.append({"role": "user", "content": input_txt})
        with st.chat_message("user"):
            st.write(input_txt)

        # Generate a response
        with st.chat_message("assistant"):
            with st.spinner("Getting your answer from superior intelligence..."):
                response = query_rag(OLLAMA_MODEL, CHROME_DB, input_txt, enable_summarization, enable_highlighting)
                st.write(response)

        # Save response to session state
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
