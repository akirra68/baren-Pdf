import fitz
import os
import sys
import subprocess
import tempfile
import msvcrt
from datetime import datetime

def processPdfs():
    if getattr(sys, 'frozen', False):
        folder_path = os.path.dirname(sys.executable)
    else:
        folder_path = os.path.dirname(os.path.abspath(__file__))

    pdf_files = [file for file in os.listdir(folder_path) if file.endswith(".pdf")]

    if not pdf_files:
        print(f"\n❌ No PDF file found in '{folder_path}', please put PDF file into this folder..\n")
        return

    selected_file = pdf_files[0]
    if len(pdf_files) > 1:
        print(f"\n⚠ Found multiple PDF files, automatically selecting : {selected_file}")  


    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, suffix=".txt") as temp_file:
        temp_filename = temp_file.name

        pdf_path = os.path.join(folder_path, selected_file)
        print(f"\n🔄 Processing file : {selected_file}")  

        temp_file.write(f"📄 File : {selected_file}\n\n\n")

        with fitz.open(pdf_path) as doc:
            for page_num, page in enumerate(doc):
                temp_file.write(f"----- Page {page_num + 1} -----\n\n")
                    
                words = [word[4] for word in page.get_text("words")] 
                counter = 1  
                    
                for i in range(0, len(words), 5): 
                    grouped_words = "⠀⠀⠀⠀⠀".join([f"{counter + j}| {words[i+j]}" for j in range(min(5, len(words) - i))])
                    temp_file.write(grouped_words + "\n\n") 
                    counter += 5 

    print("✅ Texts in file extracted successfully.\n") 

    subprocess.run(["notepad.exe", temp_filename], check=True)

    os.remove(temp_filename)

while True:
    processPdfs()

    print("Thank you for using this program :)")
    print(f"Copyright © {datetime.now().year} BarenPDF")
    print("\nPress [ENTER] to rerun the program OR Press [ESC] to exit the program..\n")

    while True:
        key = msvcrt.getch()
        if key == b'\r': 
            print("─" * 90)
            break 
        elif key == b'\x1b': 
            print("─" * 90)
            sys.exit() 
