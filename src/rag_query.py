import argparse
from langchain.prompts import ChatPromptTemplate
from config import CONFIG, PROMPT_TEMPLATE
import re




def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)



def remove_think_tags(response):
    return re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)

def query_rag(model, db, query: str, enable_summarization, enable_highlighting):
    # Prepare the DB.
    

    # Search the DB.
    results = db.similarity_search_with_score(query, k=CONFIG.TOP_K)

    # Build the context.
    context = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    # Adjust prompt template based on flags.
    extra_instructions = []
    if enable_summarization:
        extra_instructions.append("Please summarize the response.")
    if enable_highlighting:
        extra_instructions.append("Highlight the important points.")
    
    extra_instructions_text = " ".join(extra_instructions)
    prompt_template = ChatPromptTemplate.from_template(f"{PROMPT_TEMPLATE}\n{extra_instructions_text}")
    prompt = prompt_template.format(context=context, question=query)

    
    response_text = model.invoke(prompt)
    response = remove_think_tags(response_text)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response


if __name__ == "__main__":
    main()