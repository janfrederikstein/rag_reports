import os
import re
from pathlib import Path

def sort_files_by_page_number(files):
    """
    Sort .md filenames by the integer page number in 'page_X.md'.
    """
    def get_page_number(filename):
        match = re.match(r'page_(\d+)\.md$', filename)
        if match:
            return int(match.group(1))
        return float('inf')
    
    return sorted(files, key=get_page_number)

def stitch_markdown_subfolders(
    input_base_dir="pdfs/cleaned_markdown_output",
    output_base_dir="pdfs/merged_clean_markdown",
):
    """
    For each subfolder in `input_base_dir`, gather page_*.md files,
    sort them, and write them all to a single .md file in `output_base_dir`.
    """
    input_base_dir = Path(input_base_dir)
    output_base_dir = Path(output_base_dir)
    output_base_dir.mkdir(parents=True, exist_ok=True)
    
    if not input_base_dir.is_dir():
        print(f"Input directory {input_base_dir} does not exist.")
        return
    
    for subfolder in sorted(input_base_dir.iterdir()):
        if not subfolder.is_dir():
            continue
        
        # e.g., subfolder might be "pdfs/cleaned_markdown_output/file_name"
        md_files = list(subfolder.glob("*.md"))
        if not md_files:
            # No .md files in this folder, skip
            continue
        
        # Sort by the numeric page_XX
        md_filenames = [f.name for f in md_files]
        sorted_files = sort_files_by_page_number(md_filenames)
        
        # Create a single output .md file named after the folder, e.g. "file_name.md"
        output_md_file = output_base_dir / f"{subfolder.name}.md"
        
        with open(output_md_file, 'w', encoding='utf-8') as outfile:
            for filename in sorted_files:
                page_number = re.search(r'page_(\d+)\.md$', filename).group(1)
                with open(subfolder / filename, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                
                outfile.write(f"# Page {page_number}\n\n{content}\n\n")
        
        print(f"Created {output_md_file} from {subfolder.name} subfolder.")

if __name__ == "__main__":
    stitch_markdown_subfolders()
    print("All subfolders stitched into per-document markdown files.")