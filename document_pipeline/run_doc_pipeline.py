import os
from pathlib import Path

from document_pipeline.pdf_to_png_converter import convert_pdfs_to_png
from document_pipeline.png_to_markdown import process_images_recursive
from document_pipeline.cleanup_markdown import process_markdown_subfolders
from document_pipeline.merge_cleaned_markdown import merge_markdown_subfolders

def run_document_pipeline(
    pdf_input_dir="pdfs/input_dir",
    png_output_dir="pdfs/output_dir",
    md_output_dir="pdfs/markdown_output",
    cleaned_md_output_dir="pdfs/cleaned_markdown_output",
    merged_clean_md_output_dir="pdfs/merged_clean_markdown"
):
    """
    Runs the four-step pipeline in order:
      1. PDF -> PNG
      2. PNG -> MD
      3. Clean MD
      4. Merge pages into single MD per document
    """

    # Step 1: PDF -> PNG
    convert_pdfs_to_png(
        input_dir=pdf_input_dir,
        output_dir=png_output_dir,
        dpi=200
    )

    # Step 2: PNG -> MD
    process_images_recursive(
        png_input_dir=png_output_dir,
        markdown_output_dir=md_output_dir
    )

    # Step 3: Clean MD
    process_markdown_subfolders(
        input_directory_path=md_output_dir,
        output_directory_path=cleaned_md_output_dir
    )

    # Step 4: Merge MD pages
    merge_markdown_subfolders(
          input_base_dir=cleaned_md_output_dir,
          output_base_dir=merged_clean_md_output_dir
      )

    print("Pipeline completed successfully!")

if __name__ == "__main__":
    run_document_pipeline()