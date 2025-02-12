#Gộp file Titles và Number tạo thành một TOC
import os

def create_tof():
    titles_path = r"C:\Users\tanlo\OneDrive\CDHA\Books\Tiengviet\New folder\cleaned_text.txt"
    numbers_path = r"C:\Users\tanlo\OneDrive\CDHA\Books\Tiengviet\New folder\numbering.txt"
    output_path = r"C:\Users\tanlo\OneDrive\CDHA\Books\Tiengviet\New folder\TOF.txt"
    
    with open(titles_path, 'r', encoding='utf-8') as ft, \
         open(numbers_path, 'r', encoding='utf-8') as fn, \
         open(output_path, 'w', encoding='utf-8') as fo:
        titles = ft.read().splitlines()
        numbers = fn.read().splitlines()
        
        for t, n in zip(titles, numbers):
            # Convert number to int, add 6, then back to string
            new_number = str(int(n) + 6)
            # Add dots between title and number
            fo.write(f"{t}......{new_number}\n")

if __name__ == "__main__":
    create_tof()