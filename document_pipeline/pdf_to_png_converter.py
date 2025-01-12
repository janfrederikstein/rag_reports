import os
from pdf2image import convert_from_path


def convert_pdfs_to_png(input_dir: str, output_dir: str, dpi: int = 200):
    """
    Converts all PDFs in input_dir into PNG images, stored in output_dir.
    
    Args:
        input_dir (str): Path to the directory containing PDF files.
        output_dir (str): Path to the directory where PNGs should be saved.
        dpi (int): Resolution for the output images. Higher DPI = higher quality but larger file size.
    """

    # ensuring the directory exists
    os.makedirs(output_dir, exist_ok=True)

    pdf_files = [
        f for f in os.listdir(input_dir)
        if f.lower().endswith(".pdf")
    ]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)

        pdf_name = os.path.splitext(pdf_file)[0]
        output_subdir = os.path.join(output_dir, pdf_name)
        os.makedirs(output_subdir, exist_ok=True)

        print(f"Converting {pdf_file} ...")
        
        images = convert_from_path(pdf_path, dpi=dpi)

        for i, img in enumerate(images, start=1):
            output_filename = os.path.join(output_subdir, f"page_{i}.png")
            img.save(output_filename, "PNG")
        
        print(f"Finished converting {pdf_file}: output saved in {output_subdir}")