import PyPDF2
import fitz
import re


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
            pages_text.append(page.getText())

    return pages_text

def main(name_file, fixed_file, path, drawing=False, verbose=True):

    with open('{}/{}'.format(path, name_file), 'rb') as p:
        txt = (p.readlines())

    txtx = reset_eof_of_pdf_return_stream(txt)

    with open('{}/{}'.format(path, fixed_file), 'wb') as f:
        f.writelines(txtx)
      
    if drawing:
        content = extract_text_drawing_files('{}/{}'.format(path, fixed_file))
    else: 
        pdf_file = PyPDF2.PdfFileReader('{}/{}'.format(path, fixed_file))
        num_pages = pdf_file.getNumPages()
        pages = get_pages(pdf_file, num_pages)
        content = extract_text(pages)
    
    if verbose:
        print("Number pages: {}".format(len(content)))
        
    return " ".join(content)


path = '/home/cinthia/F01/'
name_file = 'test.pdf'
fixed_file= 'Licitacao_fixed.pdf'
content = main(name_file, fixed_file, path, drawing=True, verbose=True)
content = remove_noise(content)


print(content)