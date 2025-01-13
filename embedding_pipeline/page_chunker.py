import re
import logging

def chunk_markdown_by_page(md_text):
    """
    Splits the merged markdown text into page-level chunks.
    Assumes each page starts with a heading like:
        # Page 1
        # Page 2
    Returns a list of dicts: [{"page_number": int, "page_content": str}, ...]
    """
    logging.debug("Starting to chunk markdown text by page.")
    pattern = r"(^# Page\s+(\d+))"

    # using re.split with capturing parentheses to keep the split delimiter
    # returns a list where the delimiter pieces are included in the result
    parts = re.split(pattern, md_text, flags=re.MULTILINE)
    logging.debug(f"Re split into {len(parts)} parts.")


    # parts will look something like:
    # [
    #   '# Page 1', '1', <text after # Page 1 until next # Page ...>,
    #   '# Page 2', '2', <text after # Page 2 until next # Page ...>,
    #   ...
    # ]

    chunks = []
    current_page = None
    current_text = []

    # iterating over parts in steps of 3: [delimiter, page_number, chunk_text]
    idx = 0
    while idx < len(parts):
        piece = parts[idx]

        # if piece matches the pattern '# Page X'
        match = re.match(r"^# Page\s+(\d+)$", piece.strip())
        if match:
            # if there's an ongoing chunk, store it
            if current_page is not None:
                # join everything in current_text
                page_content_str = "".join(current_text).strip()
                chunks.append({
                    "page_number": current_page,
                    "page_content": page_content_str
                })
                logging.debug(f"Chunk created for page {current_page} with {len(page_content_str)} characters.")

            

            current_page = int(match.group(1))
            logging.debug(f"Detected new page: {current_page}.")
            current_text = []
            
            idx += 1  # skip the page number capturing group
        else:
            current_text.append(piece)
        
        idx += 1
    
    # one last page's content to store after the loop
    if current_page is not None and current_text:
        page_content_str = "".join(current_text).strip()
        chunks.append({
            "page_number": current_page,
            "page_content": page_content_str
        })
        logging.debug(f"Final chunk created for page {current_page} with {len(page_content_str)} characters.")

    logging.info(f"Created {len(chunks)} page chunks.")
    return chunks