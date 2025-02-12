#Lọc nội dung Titles, loại bỏ số và các dòng trắng, space đầu dòng
import PyPDF2
import re
import os
import string

def extract_and_clean_text(
    pdf_path=r"C:\Users\tanlo\OneDrive\CDHA\Books\Tiengviet\cc.pdf",
    output_folder=r"C:\Users\tanlo\OneDrive\CDHA\Books\Tiengviet\New folder",
    start_page=3,
    end_page=6
):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    reader = PyPDF2.PdfReader(pdf_path)
    extracted_text = []
    for page_num in range(start_page - 1, end_page):
        if page_num < len(reader.pages):
            page_text = reader.pages[page_num].extract_text()
            # Remove Roman numerals and numbers
            page_text = re.sub(r"\b[IVXLCDMivxlcdm]+\b|\d+", "", page_text)
            # Remove punctuation marks
            page_text = page_text.translate(str.maketrans("", "", string.punctuation))
            # Split into lines, clean and filter empty lines
            lines = [line.strip() for line in page_text.splitlines()]
            cleaned_lines = [line for line in lines if line]
            if cleaned_lines:
                extracted_text.append('\n'.join(cleaned_lines))

    output_file = os.path.join(output_folder, "cleaned_text.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write('\n'.join(extracted_text))

if __name__ == "__main__":
    extract_and_clean_text()