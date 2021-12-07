import PyPDF2
import fitz
import re
import pandas as pd
import cv2
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import numpy as np

def remove_noise(text):
    text = re.sub('\n', ' ', text)
    return text

def get_pages(pdf_file, num_pages):
    pages = [pdf_file.getPage(i) for i in range(num_pages)]
    return pages

def extract_text(pages):
    texts = [page.extractText() for page in pages]
    return texts

def reset_eof_of_pdf_return_stream(pdf_stream_in:list):
    # find the line position of the EOF
    for i, x in enumerate(pdf_stream_in[::-1]):
        if b'%%EOF' in x:
            actual_line = len(pdf_stream_in)-i
            break

    # return the list up to that point
    return pdf_stream_in[:actual_line]

def extract_text_drawing_files(path):

    with fitz.open(path) as doc:
        pages_text = []
        for page in doc:
            pages_text.append(page.get_text())

    return pages_text

def pdf_to_text(name_file, fixed_file, path, drawing=False, verbose=True):

    # with open(name_file, 'rb') as p:
    #     txt = (p.readlines())

    # txtx = reset_eof_of_pdf_return_stream(txt)

    # with open('{}/{}'.format(path, fixed_file), 'wb') as f:
    #     f.writelines(txtx)
      
    if drawing:
        content = extract_text_drawing_files(name_file)
    else: 
        pdf_file = PyPDF2.PdfFileReader(name_file)
        num_pages = pdf_file.getNumPages()
        pages = get_pages(pdf_file, num_pages)
        content = extract_text(pages)
    
    if verbose:
        print("Number pages: {}".format(len(content)))
        
    return " ".join(content)

def pdf_from_image(file, verbose=False):
    pages = convert_from_path(file, 350)
    text = ""
    for page in pages:

        # Treatment

        # convertendo em um array editável de numpy[x, y, CANALS]
        npimagem = np.asarray(page).astype(np.uint8)  

        # diminuição dos ruidos antes da binarização
        npimagem[:, :, 0] = 0 # resetting the R channel (RED)
        npimagem[:, :, 2] = 0 # resetting channel B (BLUE)

        # grayscale assignment
        im = cv2.cvtColor(npimagem, cv2.COLOR_RGB2GRAY) 

        # application of binary truncation to intensity
        # pixels of color depth below 127 will be converted to 0 (BLACK)
        # pixels of color depth above 127 will be converted to 255 (WHITE)
        # The assignment of THRESH_OTSU enhances an intelligent analysis of the levels of truncation 
        ret, thresh = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) 

        binimagem = Image.fromarray(thresh) 

        # Tesseract OCR
        text += pytesseract.image_to_string(binimagem, lang='por')  
        binimagem.close()

    text = remove_noise(text)
    if verbose:
        print(text)
    return text

# path = '/home/cinthia/F01/'
# path = '/home/asafe/GitHub/Coleta_C01/Para_de_Minas/esic/data/files/'
# name_file = '2f37e03c3179bb4f1312f2093f6742af.pdf.pdf'
fixed_file= 'Licitacao_fixed.pdf'

def count_matches (text, keyword_to_search):

    matches = 0
    for i in keyword_to_search:
        matches += text.lower().count(i.lower())

    return matches

def analyze_pdf(path_base, pdf_files, keyword_to_search, verbose=False):

    matches = []

    for file in pdf_files:
        print("aux:", file, "***********")
        content = pdf_to_text(file, fixed_file, path_base, drawing=True, verbose=False)
        content = remove_noise(content)
        # print(path_functions.get_url("/home/asafe", path), count_matches (text, keyword_to_search))

        num_matches =  count_matches (content, keyword_to_search)

        # In case you have not found the keywords, we will do the search with OCR
        if (num_matches == 0):
            content = pdf_from_image(file, verbose)
            num_matches = count_matches (content, keyword_to_search)

        matches.append(num_matches)
    
    result = pd.DataFrame({'files': pdf_files, 'matches': matches})

    return result
