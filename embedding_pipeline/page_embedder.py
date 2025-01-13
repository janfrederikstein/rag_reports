import openai
import logging
from typing import List, Dict

def embed_pages(page_chunks: List[Dict], openai_api_key: str):
    """
    Takes a list of page-level chunks:
      [{"page_number": 1, "page_content": "..."}, ...]
    and returns a list of dicts, each containing:
      {"page_number": int, "embedding": [...], "text": str}
    
    Uses OpenAI 'text-embedding-ada-002' by default
    """
    logging.info("Starting to embed pages.")

    embeddings_data = []
    for chunk in page_chunks:
        page_text = chunk["page_content"]
        page_num = chunk["page_number"]
        logging.debug(f"Embedding page {page_num} with {len(page_text)} characters.")

        # API call to generate the embedding
        try:
            response = openai.embeddings.create(
                model="text-embedding-ada-002",
                input=page_text
            )
            embedding_vector = response.data[0].embedding
            logging.debug(f"Received embedding of length {len(embedding_vector)} for page {page_num}.")
        except Exception as e:
            logging.exception(f"Error embedding page {page_num}: {e}")
            continue

        embeddings_data.append({
            "page_number": page_num,
            "embedding": embedding_vector,
            "text": page_text
        })    
        
    logging.info(f"Embedded {len(embeddings_data)} pages successfully.")
    return embeddings_data

