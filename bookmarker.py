import re
import os
import sys
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

import fitz  # PyMuPDF

def extract_text_from_pages(pdf_path, start_page, end_page):
    """Extract text from the specified page range of a PDF file."""
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(start_page - 1, min(end_page, len(doc))):
            page = doc[page_num]
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

def parse_toc(toc_text):
    """Parse the table of contents text to extract chapter titles and page numbers."""
    # Pattern to match chapter title followed by page number
    # This pattern searches for text followed by dots and then numbers at the end of the line
    pattern = r'(.*?\.{2,}|.*?\s)\s*(\d+)\s*$'
    
    bookmarks = []
    for line in toc_text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        match = re.search(pattern, line)
        if match:
            title = match.group(1).strip().rstrip('.')
            page_num = int(match.group(2))
            
            # Clean up the title (remove trailing dots, extra spaces)
            title = re.sub(r'\.+$', '', title).strip()
            
            bookmarks.append((title, page_num))
    
    return bookmarks

def add_bookmarks_to_pdf(input_path, bookmarks, page_offset, output_path=None):
    """Add bookmarks to the PDF and save as a new file."""
    if output_path is None:
        # Create output filename with "_bookmarked" suffix
        output_path = os.path.splitext(input_path)[0] + "_bookmarked.pdf"
    
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    # Copy all pages from the original PDF
    for page in reader.pages:
        writer.add_page(page)
    
    # Add bookmarks
    for title, page_num in bookmarks:
        # Adjust page number with offset
        adjusted_page = page_num + page_offset - 1  # -1 because PDF pages are 0-indexed
        if 0 <= adjusted_page < len(reader.pages):
            writer.add_outline_item(title, adjusted_page)
    
    # Save the output file
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)
    
    return output_path

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Select PDF file
    pdf_path = filedialog.askopenfilename(
        title="Chọn file PDF",
        filetypes=[("PDF files", "*.pdf")]
    )
    
    if not pdf_path:
        messagebox.showinfo("Thông báo", "Không có file nào được chọn.")
        return
    
    # Get TOC page range
    start_page = simpledialog.askinteger("Nhập thông tin", "Nhập trang bắt đầu của mục lục:")
    if start_page is None:
        return
        
    end_page = simpledialog.askinteger("Nhập thông tin", "Nhập trang kết thúc của mục lục:")
    if end_page is None:
        return
    
    # Get page offset
    page_offset = simpledialog.askinteger("Nhập thông tin", 
        "Nhập số trang chênh lệch (số trang thực tế - số trang trong mục lục):")
    if page_offset is None:
        return
    
    # Extract TOC text
    toc_text = extract_text_from_pages(pdf_path, start_page, end_page)
    
    if not toc_text:
        messagebox.showerror("Lỗi", "Không thể đọc được mục lục!")
        return
    
    # Parse TOC
    bookmarks = parse_toc(toc_text)
    
    if not bookmarks:
        messagebox.showerror("Lỗi", "Không tìm thấy bookmark nào từ mục lục!")
        return
    
    # Process and save the PDF with bookmarks
    try:
        output_path = add_bookmarks_to_pdf(pdf_path, bookmarks, page_offset)
        messagebox.showinfo("Thành công", f"Đã thêm {len(bookmarks)} bookmark và lưu tại:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")

if __name__ == "__main__":
    main()
