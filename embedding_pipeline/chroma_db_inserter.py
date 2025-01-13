import logging

def insert_into_chromadb(embedded_pages, collection):
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
            collection.add(
                embeddings=[page_data["embedding"]],
                documents=[page_data["text"]],
                metadatas=[{"page_number": page_data["page_number"]}],
                ids=[f"doc_page_{i}"]
            )
            logging.debug(f"Inserted page {page_data['page_number']} (doc_page_{i}).")
        except Exception as e:
            logging.exception(f"Failed to insert page {page_data['page_number']} (doc_page_{i}): {e}")

    logging.info(f"Inserted {len(embedded_pages)} pages into collection '{collection.name}'.")
    print(f"Inserted {len(embedded_pages)} pages into collection '{collection.name}'.")