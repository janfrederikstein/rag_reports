import os
from pathlib import Path
import logging
import openai

from .page_chunker import chunk_markdown_by_page
from .page_embedder import embed_pages
from .chroma_db_inserter import insert_into_chromadb

import chromadb
from chromadb.config import Settings

from dotenv import load_dotenv
load_dotenv()

log_file = "embedding_pipeline.log"
logging.basicConfig(
    level=logging.DEBUG,  # adjust as needed (DEBUG, INFO, WARNING, ERROR)
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        # logging.StreamHandler()
    ]
)

logging.info("Logging configured. Running embedding pipeline.")


def run_embedding_pipeline(
    openai_api_key,
    md_directory: str = "pdfs/merged_clean_markdown",
    chroma_db_dir: str = "chromadb_store",
    collection_name: str = "financial_reports",
):
    """
    processes all .md files in md_directory:
      1) For each .md, chunk it by page
      2) Embed each page
      3) Insert embeddings into ChromaDB
    """
    logging.info("Pipeline started.")

    md_path = Path(md_directory)
    if not md_path.is_dir():
        error_msg = f"Markdown directory not found: {md_path}"
        logging.error(error_msg)
        raise NotADirectoryError(f"Markdown directory not found: {md_path}")


    # gather all .md files in dir
    md_files = sorted(md_path.glob("*.md"))
    if not md_files:
        logging.warning(f"No .md files found in {md_path}. Nothing to process.")
        print(f"No .md files found in {md_path}. Nothing to process.")
        return

    persist_directory = Path(chroma_db_dir).resolve()
    persist_directory.mkdir(parents=True, exist_ok=True)
    logging.info(f"ChromaDB store path resolved to: {persist_directory}")


    client = chromadb.PersistentClient(
        path=str(persist_directory),
        settings=Settings(allow_reset=True)
    ) # creates file chroma.sqlite3 if it does not exist

    logging.info(f"ChromaDB client created with persist_directory: {persist_directory}")
    print("ChromaDB client created with persist_directory:", Path(chroma_db_dir).resolve())

    collection = client.get_or_create_collection(collection_name)
    logging.info(f"Using collection: '{collection.name}'.")
    print(f"Using collection: '{collection.name}'.")

    for file in md_files:
        print(f"\nProcessing {file.name}...")
        with open(file, "r", encoding="utf-8") as f:
            md_text = f.read()

        # chunking by page
        logging.info("Chunking markdown by page.")
        page_chunks = chunk_markdown_by_page(md_text)

        # embedding each page
        logging.info(f"Found {len(page_chunks)} page chunks in {file.name}.")
        logging.info("Embedding each page.")
        embedded_pages = embed_pages(page_chunks, openai_api_key=openai_api_key)

        # inserting embeddings into ChromaDB
        logging.info("Inserting embeddings into ChromaDB.")
        insert_into_chromadb(embedded_pages, collection)

        logging.info(f"Finished embedding {len(embedded_pages)} pages from {file.name}.")
        print(f"Finished embedding {len(embedded_pages)} pages from {file.name}.")

    logging.info("All Markdown files processed successfully!")
    print("\nAll Markdown files processed successfully!")



if __name__ == "__main__":
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        logging.error("OPENAI_API_KEY not found, check .env file.")
        raise ValueError("OPENAI_API_KEY not found, check .env file.")

    try:
        run_embedding_pipeline(openai_api_key)
    except Exception as e:
        logging.exception("An error occurred in the embedding pipeline.")

