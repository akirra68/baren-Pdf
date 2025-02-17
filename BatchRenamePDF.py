import os
import fitz
import re
import msvcrt

folder_path = "D:/TEST"
format_text_name = "Name :"
format_text_no = "No. :"

for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(folder_path, filename)

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
                print(f"{running}. ✅ '{filename}', Successfully created new file: '{new_filename}'")

            elif not match_name and match_no:
                print(f"❌ '{format_text_name}' not found in '{filename}', skipping file.")

            elif match_name and not match_no:
                print(f"❌ '{format_text_no}' not found in '{filename}', skipping file.")

            else:
                print(f"❌ Both '{format_text_name}' and '{format_text_no}' not found in '{filename}', skipping file.")

print("\nThank you for using this program:)")
print("❤️ Made with love by AKIRRA ❤️")

print("\nPress (ESC) to exit the program...")
while True:
    key = msvcrt.getch()
    if key == b'\x1b':  
        break