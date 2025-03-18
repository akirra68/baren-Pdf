import fitz 

def get_text_after_keyword(page, keyword1, keyword2):
    words = page.get_text("words")  
    for i in range(len(words) - 1):  
        if words[i][4] == keyword1 and words[i + 1][4] == keyword2:  
            if i + 2 < len(words):  
                return words[i + 2][4]  
    return None 

def get_text_before_keyword(page, keyword1, keyword2):
    words = page.get_text("words")
    for i in range(1, len(words)): 
        if words[i-1][4] == keyword1 and words[i][4] == keyword2:
            if i - 2 >= 0: 
                return words[i - 2][4]  
    return None

pdf_path = "TEST.pdf"
doc = fitz.open(pdf_path)
page = doc[0]  

nomor_value = get_text_after_keyword(page, "NOMOR", "UNIK")
tahun_value = get_text_before_keyword(page, "TIDAK", "FINAL")
nama_value = get_text_after_keyword(page, "NAMA", ":")

print(f"NOMOR: {nomor_value}")
print(f"MASA PAJAK: {tahun_value}")
print(f"NAMA: {nama_value}")

doc.close()
