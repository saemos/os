import os
from pypdf import PdfReader

def extract_pdf_to_text(pdf_path, output_txt_path="data/book_data.txt"):
    print(f"[Automation] Reading PDF file from: {pdf_path}")
    if not os.path.exists(pdf_path):
        print(f"[Error] PDF file not found at {pdf_path}")
        return

    reader = PdfReader(pdf_path)
    extracted_text = ""

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            extracted_text += f"\n--- Page {i+1} ---\n" + text

    # Automatically save to your bot's readable text format
    os.makedirs(os.path.dirname(output_txt_path), exist_ok=True)
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)

    print(f"[Automation] Successfully extracted {len(reader.pages)} pages into {output_txt_path}!")

if __name__ == "__main__":
    # Point this to your PDF file inside your workspace
    target_pdf = "data/raw_books/physics_chapter.pdf"
    extract_pdf_to_text(target_pdf)
