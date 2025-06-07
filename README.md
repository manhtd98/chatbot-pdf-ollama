# RAG_Ollama_Deepseek_Streamlit
 Local RAG Chatbot leveraging 
Before getting started, ensure you have the following installed:

* **Python 3.7+:** Python is required for running the application.
* **Ollama:** Download and install Ollama from ([https://ollama.com/]).
* ChromaDB
* langchain
* Streamlit
* **Pip:** Python package installer.

## 4. Installation

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/pruthvirajcyn/RAG_Ollama_Deepseek_Streamlit.git
    cd RAG_Ollama_Deepseek_Streamlit
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r .\src\requirements.txt
    ```

## 5. Usage

1.  **Run Ollama:**
    In another tab of command prompt/ terminal run the below
    ```bash
    ollama pull nomic-embed-text
    ollama pull qwen3:4b
    ollama serve
    ```

4.  **Run the Streamlit Application:**

    ```bash
    streamlit run app.py
    ```
    
6.  **Chat with the Bot:**

    Enter your queries in the chat input and receive responses augmented with information from your documents.

## 6. Customization

* **Modify Prompts:** Edit the prompt templates in `app.py` to customize the chatbot's behavior.
* **Change Models:** You can replace DeepSeek-R1 with other models supported by Ollama. Remember to update the Ollama pull command and the model name in the code.
* **Adjust Retrieval Parameters:** Fine-tune the retrieval parameters in the code to optimize document retrieval.
* **Extend Functionality:** Add more features to the Streamlit interface or integrate with other tools.

## 7. Troubleshooting

* **Ollama Issues:** If you encounter issues with Ollama, refer to the official Ollama documentation.
* **Dependency Issues:** Ensure all dependencies are installed correctly. If you encounter errors, try reinstalling the virtual environment.
* **Model Loading Issues:** Verify that the DeepSeek-R1 model is pulled correctly in Ollama.

