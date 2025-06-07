from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
import os

def pdf_load(file_name):
    document_loader = PyPDFLoader(file_name)
    return document_loader.load()

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def add_to_db(CHROME_DB, chunks: list[Document]):
    # Load the existing database.
    
    chunks_with_ids = calculate_chunk_ids(chunks) # Giving each chunk an ID

    
    # Add or Update the documents.
    existing_items = CHROME_DB.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        CHROME_DB.add_documents(new_chunks, ids=new_chunk_ids)
        CHROME_DB.persist()
    else:
        print(" all documents are added")



def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks

def document_load_pdf(CHROME_DB, file_name):
    # Check if the database should be cleared (using the --clear flag).
    for collection in CHROME_DB._client.list_collections():
        ids = collection.get()['ids']
        print('REMOVE %s document(s) from %s collection' % (str(len(ids)), collection.name))
    if len(ids): collection.delete(ids)
    print("All data in the Chroma database has been cleared.")
    documents = pdf_load(file_name)
    chunks = split_documents(documents)
    add_to_db(CHROME_DB, chunks)


if __name__ == "__main__":
    document_load_pdf()