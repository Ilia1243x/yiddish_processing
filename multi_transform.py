import sys
import os
from pdf2image import convert_from_path
from pytesseract import image_to_string
from PIL import Image
from PyPDF2 import PdfReader
from multiprocessing import Pool, cpu_count

def translate_file(file_i):
    pdf_path = 'C:/Users/Ilia2024/Desktop/yiddish/texts_pdf/texts (2100)'
    root_path = 'C:/Users/Ilia2024/Desktop/yiddish/texts_txt/'
    
    file_path = os.path.join(pdf_path, file_i)

    number = len(PdfReader(file_path).pages)
    
    name = file_i[:-3] + "txt"

    print(name, number)
    
    txt_path = os.path.join(root_path, name)

    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        for j in range(0, number, 30):
            #print(j, j+10)
            full_text = ""
            pages = convert_from_path(file_path, dpi = 300, first_page = j, last_page = min(j+30,number-1))
            for page in pages:
                full_text += image_to_string(page, lang ='yid')
            txt_file.write(full_text)
    print(name)
    
if __name__ == "__main__":
    pdf_path = 'C:/Users/Ilia2024/Desktop/yiddish/texts_pdf/texts (2100)'
    files = os.listdir(pdf_path)
    files = sorted(files)
    num_proc = 6
    selected = files[210:460]

    p = Pool(num_proc)
    p.map(translate_file, selected)
