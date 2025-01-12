import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)



def clean_markdown_content(text):
    """
    Sends the markdown text to OpenAI to remove irrelevant content.
    """

    response = client.chat.completions.create(model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": (
                "You are tasked with cleaning up the following markdown text. "
                "You should return only the cleaned-up markdown text. Do not explain your "
                "output or reasoning. Remove any irrelevant text from the markdown, "
                "such as embedded images ([ ]( )), references to 'click here', 'Listen to this article', "
                "page numbers, or logos. Only return the cleaned-up content."
            )
        },
        {
            "role": "user",
            "content": text,
        }
    ],
    max_tokens=4096,
    temperature=0  # for deterministic output
    )

    try:
        cleaned_content = response.choices[0].message.content
    except (AttributeError, IndexError, KeyError):
        cleaned_content = "Error: Could not parse the response from the model."

    return cleaned_content

def process_markdown_subfolders(
    input_directory_path="pdfs/markdown_output",
    output_directory_path="pdfs/cleaned_markdown_output"
):
    """
    Recursively process subfolders in `input_directory_path` for .md files,
    clean their content via OpenAI, and save to matching subfolders in `output_directory_path`.
    """
    input_dir = Path(input_directory_path)
    output_dir = Path(output_directory_path)

    # creating the top-level output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_dir.exists():
        print(f"The directory {input_dir} does not exist.")
        return

    # Example: 
    # pdfs/markdown_output/
    #   SomeReport/
    #       page_1.md
    #       page_2.md
    #   AnotherReport/
    #       page_1.md
    #       ...

    for pdf_subfolder in sorted(input_dir.iterdir()):
        if not pdf_subfolder.is_dir():
            continue

        # creating a matching subfolder in the output directory
        cleaned_subfolder = output_dir / pdf_subfolder.name
        cleaned_subfolder.mkdir(parents=True, exist_ok=True)

        md_files = sorted(pdf_subfolder.glob("*.md"))
        for md_file in md_files:
            print(f"Cleaning {md_file}...")

            # read the existing markdown
            with open(md_file, "r", encoding="utf-8") as file:
                content = file.read()

            # calling llm to clean it up
            cleaned_content = clean_markdown_content(content)

            # writing the cleaned version to a new .md file
            cleaned_file_path = cleaned_subfolder / md_file.name
            with open(cleaned_file_path, "w", encoding="utf-8") as out_file:
                out_file.write(cleaned_content)

            print(f"→ Cleaned content saved to {cleaned_file_path}")

    print("All markdown files cleaned successfully!")