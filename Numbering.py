#từ OCR dãy các số trang, loại bỏ các dòng trắng
with open(r"C:\Users\tanlo\OneDrive\CDHA\Books\Tiengviet\New folder\numbering.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(r"C:\Users\tanlo\OneDrive\CDHA\Books\Tiengviet\New folder\numbering.txt", "w", encoding="utf-8") as f:
    for line in lines:
        if line.strip():
            f.write(line)