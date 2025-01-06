# rag_reports
RAG application designed to query financial report PDFs


# Initializing

#### activating venv
source venv/bin/activate

#### installing system level dependencies
%brew install poppler tesseract libmagic


## Pre-processing PDFs
Before the pdf content can be embedded into a vector store, it needs to be extracted properly from the pdf files.
The document_pipeline package contains a full document extraction pipeline that:
1. Converts document pages to PNG files.
2. Sends the PNG files to GPT-4o (vision model) to extract the contents as Markdown
3. Cleans the markdown pages, using GPT-4o-mini
4. Merges the files back together to one full Markdown version of the original document

#### Running the pipeline
run_doc_pipeline.py will sequentially execute this process. Note that it currently is not set up to avoid duplicates if the documents have already been processed earlier.


### Running Streamlit app
streamlit run <path>/streamlit_app.py