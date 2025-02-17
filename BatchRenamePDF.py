import os
import sys
import fitz
import re
import msvcrt

if getattr(sys, 'frozen', False):
    folder_path = os.path.dirname(sys.executable)
else:
    folder_path = os.path.dirname(os.path.abspath(__file__))
format_text_name = "Name :"
format_text_no = "No. :"

pdf_files = [file for file in os.listdir(folder_path) if file.endswith(".pdf")]

def exit_program():
    print("\nThank you for using this program :)")
    print("❤️ Made with love by AKIRRA ❤️")

    print("\nPress (ESC) to exit the program...")
    while True:
        key = msvcrt.getch()
        if key == b'\x1b': 
            break

if not pdf_files:
    print("─" * 90)
    print(f"❌ No PDF files found in the folder ({folder_path}). Exiting program..")
    print("─" * 90)
    exit_program()
    exit()

print("─" * 90)
for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(folder_path, filename)
        print(f"📄 Processing file: {pdf_path}")

        with fitz.open(pdf_path) as doc:
            text = "".join([page.get_text("text") for page in doc])

            match_name = re.search(re.escape(format_text_name) + r"\s*(\w+\s*\w*)", text)
            match_no = re.search(re.escape(format_text_no) + r"\s*(\d+)", text)

            if match_name and match_no:
                name = match_name.group(1).strip().replace(" ", "-")
                no = match_no.group(1).strip()
                new_filename = f"{name}_{no}.pdf"
                new_path = os.path.join(folder_path, new_filename)
                counter = 1
                running = 1

                while os.path.exists(new_path):
                    new_filename = f"{name}_{no}_{counter}.pdf"
                    new_path = os.path.join(folder_path, new_filename)
                    counter += 1
                    running += 1

                doc.save(new_path)
                print(f"{running}. ✅ Successfully created new file: '{new_filename}'")
                print("─" * 90)

            elif not match_name and match_no:
                print(f"❌ '{format_text_name}' not found in '{filename}', skipping file.")
                print("─" * 90)

            elif match_name and not match_no:
                print(f"❌ '{format_text_no}' not found in '{filename}', skipping file.")
                print("─" * 90)

            else:
                print(f"❌ Both '{format_text_name}' and '{format_text_no}' not found in '{filename}', skipping file.")
                print("─" * 90)

exit_program()