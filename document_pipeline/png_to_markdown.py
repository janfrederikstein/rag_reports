import os
import base64
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

def encode_image_to_base64(image_path):
    """
    Reads an image file from disk and encodes it as a base64 string.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def image_to_markdown(base64_image):
    """
    Sends the base64-encoded image to the GPT-4 Vision endpoint
    and returns the Markdown text output.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-turbo",  # model name
        "messages": [{
            "role": "user",
            "content": [{
                "type": "text",
                "text": (
                    "Give me the markdown text output from this page in a PDF using formatting "
                    "to match the structure of the page as closely as you can. Only output the "
                    "markdown and nothing else. Do not explain the output, just return it. "
                    "Do not use a single # for a heading. All headings will start with ## or ###. "
                    "Convert tables to markdown tables. Describe charts as best you can. "
                    "DO NOT return in a code block. Just return the raw text in markdown format."
                )
            }, {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"
                }
            }]
        }],
        "max_tokens": 4096
    }

    # posting the request to the chat completions endpoint
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    response_json = response.json()

    # error handling
    if "choices" not in response_json:
        raise RuntimeError(f"API response error: {response_json}")

    return response_json["choices"][0]["message"]["content"]

def process_images_recursive(
    png_input_dir="pdfs/output_dir",
    markdown_output_dir="pdfs/markdown_output"
):
    """
    Recursively finds PNG files in `png_input_dir` organized by PDF name subfolders,
    converts each PNG to Markdown using the OpenAI vision model,
    and saves the output in matching subfolders in `markdown_output_dir`.
    """
    # making sure the top-level markdown output folder exists
    os.makedirs(markdown_output_dir, exist_ok=True)

    input_path = Path(png_input_dir)
    if not input_path.exists():
        print(f"Input directory {input_path} does not exist.")
        return

    # example folder structure:
    # png_output/
    #   report_2020/
    #       page_1.png
    #       page_2.png
    #   report_2021/
    #       page_1.png
    #       ...
    #
    # mirroring that structure in markdown_output_dir

    for pdf_subfolder in sorted(input_path.iterdir()):
        # Skip if not a directory
        if not pdf_subfolder.is_dir():
            continue

        # creating a corresponding subfolder in markdown directory
        output_subfolder = Path(markdown_output_dir) / pdf_subfolder.name
        os.makedirs(output_subfolder, exist_ok=True)

        # all .png files in subfolder
        png_files = sorted(pdf_subfolder.glob("*.png"))

        for png_file in png_files:
            print(f"Processing {png_file}...")

            # encoding image to base64
            encoded_img = encode_image_to_base64(png_file)

            # calling vision model to convert to markdown
            markdown_content = image_to_markdown(encoded_img)

            # creating output path for markdown file
            md_output_path = output_subfolder / f"{png_file.stem}.md"
            with open(md_output_path, "w") as f:
                f.write(markdown_content)

            print(f"→ Saved {md_output_path}")

    print("All images converted to Markdown successfully!")