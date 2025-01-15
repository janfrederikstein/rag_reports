import logging

def insert_into_chromadb(embedded_pages, collection, doc_name):
    """
    inserts the list of embedded_pages into the provided ChromaDB collection
    
    each element in embedded_pages is expected to be a dict containing:
      - "page_number": int
      - "embedding": List[float]
      - "text": str
    """
    logging.info("Inserting pages into ChromaDB collection.")

    for i, page_data in enumerate(embedded_pages):
        try:
            metadata = {
                "page_number": page_data["page_number"],
                "doc_name": doc_name
            }

            collection.add(
                embeddings=[page_data["embedding"]],
                documents=[page_data["text"]],
                metadatas=[metadata],
                ids=[f"{doc_name}_page_{i}"]
            )
            logging.debug(f"Inserted page {page_data['page_number']} (doc_page_{i}) from document '{doc_name}'.")
        except Exception as e:
            logging.exception(f"Failed to insert page {page_data['page_number']} (doc_page_{i}) from document '{doc_name}': {e}")

    logging.info(f"Inserted {len(embedded_pages)} pages into collection '{collection.name}' for document '{doc_name}'.")
    print(f"Inserted {len(embedded_pages)} pages into collection '{collection.name}' for document '{doc_name}'.")