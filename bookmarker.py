#áp file TOF đã gộp vào file PDF
from PyPDF2 import PdfReader, PdfWriter
import os

def add_bookmarks():
    # File paths
    tof_path = r"C:\Users\tanlo\OneDrive\CDHA\Books\Tiengviet\New folder\TOF.txt"
    pdf_path = r"C:\Users\tanlo\OneDrive\CDHA\Books\Tiengviet\cc.pdf"
    output_folder = r"C:\Users\tanlo\OneDrive\CDHA\Books\Tiengviet\New folder"
    output_path = os.path.join(output_folder, "bookmarked_output.pdf")

    # Read the TOF file
    with open(tof_path, 'r', encoding='utf-8') as f:
        bookmarks = []
        for line in f:
            title, page = line.strip().split('......')
            bookmarks.append((title.strip(), int(page)))

    # Process PDF
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Copy pages
    for page in reader.pages:
        writer.add_page(page)

    # Add bookmarks
    for title, page in bookmarks:
        writer.add_outline_item(title, page - 1)  # PDF pages are 0-based

    # Save the output
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

if __name__ == "__main__":
    add_bookmarks()