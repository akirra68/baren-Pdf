import os
import sys
import fitz
import msvcrt
from datetime import datetime

def getTextBeforeKey(page, keywords):
    words = page.get_text("words")
    for i in range(len(words) - len(keywords)):
        if all(words[i + j][4] == keywords[j] for j in range(len(keywords))):
            if i - 1 >= 0:
                return words[i - 1][4]
    return None

def getTextAfterKey(page, keywords):
    words = page.get_text("words")
    for i in range(len(words) - len(keywords)):
        if all(words[i + j][4] == keywords[j] for j in range(len(keywords))):
            if i + len(keywords) < len(words):
                return words[i + len(keywords)][4]
    return None

def getFullNameAfterKey(page, keywords):
    words = page.get_text("words")
    for i in range(len(words) - len(keywords)):
        if all(words[i + j][4] == keywords[j] for j in range(len(keywords))):
            if i + len(keywords) < len(words):
                extracted_text = []
                first_line = words[i + len(keywords)][6] 
                for j in range(i + len(keywords), len(words)):
                    if words[j][6] != first_line: 
                        break
                    extracted_text.append(words[j][4])
                return "-".join(extracted_text).strip()
    return None

def getUserInput(prompt):
    return input(prompt).strip()

while True:
    try:
        if getattr(sys, 'frozen', False):
            folder_path = os.path.dirname(sys.executable)
        else:
            folder_path = os.path.dirname(os.path.abspath(__file__))

        keys = []
        while len(keys) < 3:
            print("─" * 90)
            key_texts = getUserInput("\nEnter Key texts (or leave blank to skip) : ")
            if not key_texts:
                break 

            print(f"\nThe index of Value texts is (...) '{key_texts}'.")
            print("1. BEFORE")
            print("2. AFTER")
            print("3. NAME")

            while True:
                choice = getUserInput("Enter your choice (1/2/3) : ")
                if choice in ["1", "2", "3"]:
                    break
                print("\n❌ Invalid choice. Please enter 1, 2, or 3.")

            if choice == "1":
                keys.append(("before", key_texts.split()))
            elif choice == "2":
                keys.append(("after", key_texts.split()))
            elif choice == "3":
                keys.append(("name", key_texts.split()))

        if not keys:
            print("─" * 90)
            print("❌ No valid Key texts provided.")
            print("─" * 90)
            raise Exception() 

        pdf_files = [file for file in os.listdir(folder_path) if file.endswith(".pdf")]

        if not pdf_files:
            print("─" * 90)
            print(f"❌ No PDF file found in '{folder_path}', please put PDF file into this folder...")
            print("─" * 90)
            raise Exception()

        print("─" * 90)
        for filename in pdf_files:
            pdf_path = os.path.join(folder_path, filename)
            print(f"🔄 Processing file : '{filename}'")

            with fitz.open(pdf_path) as doc:
                page = doc[0]

                extracted_values = [] 
                missing_keys = [] 

                for mode, keywords in keys:
                    if mode == "before":
                        value = getTextBeforeKey(page, keywords)
                    elif mode == "after":
                        value = getTextAfterKey(page, keywords)
                    elif mode == "name":
                        value = getFullNameAfterKey(page, keywords)
                    else:
                        value = None

                    if value:
                        extracted_values.append(value)
                    else:
                        missing_keys.append(" ".join(keywords))

                if missing_keys:
                    if len(missing_keys) == 1:
                        error_message = f"❌ Key text '{missing_keys[0]}' not found in '{filename}', skipping file."
                    elif len(missing_keys) == 2:
                        error_message = f"❌ Key text '{missing_keys[0]}' and '{missing_keys[1]}' not found in '{filename}', skipping file."
                    else:
                        error_message = f"❌ Key texts {', '.join(missing_keys[:-1])}, and '{missing_keys[-1]}' not found in '{filename}', skipping file."

                    print(error_message)
                    print("─" * 90)
                    raise Exception()

                new_filename = "_".join(extracted_values) + ".pdf"
                new_path = os.path.join(folder_path, new_filename)

                # Hindari nama file duplikat
                counter = 1
                while os.path.exists(new_path):
                    new_filename = "_".join(extracted_values) + f"_{counter}.pdf"
                    new_path = os.path.join(folder_path, new_filename)
                    counter += 1

                doc.save(new_path)
                print(f"✅ {counter}. Successfully created new file: '{new_filename}'")
                print("─" * 90)

    except:
        pass  # tangkap error dan lanjutkan ke opsi rerun/exit

    print("\nThank you for using this program :)")
    print(f"Copyright © {datetime.now().year} BarenPDF")
    print("\nPress [ENTER] to rerun the program OR Press [ESC] to exit the program..\n")

    while True:
        key = msvcrt.getch()
        if key == b'\r':        # ENTER KEY
            break 
        elif key == b'\x1b':    # ESC KEY
            sys.exit()
