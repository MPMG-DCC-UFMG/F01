import PyPDF2
import re


def remove_noise(text):
    
    text = re.sub('\n', '', text)
    
    return text


def get_pages(pdf_file, num_pages):
    
    pages = [pdf_file.getPage(i) for i in range(num_pages)]
    
    return pages


def extract_text(pages):
    
    texts = [page.extractText() for page in pages]
    print(texts)
    
    return texts

def reset_eof_of_pdf_return_stream(pdf_stream_in:list):
    # find the line position of the EOF
    for i, x in enumerate(pdf_stream_in[::-1]):
        if b'%%EOF' in x:
            actual_line = len(pdf_stream_in)-i
            break

    # return the list up to that point
    return pdf_stream_in[:actual_line]


def main(name_file, fixed_file, path, verbose=True):
    # with open('{}/{}'.format(path, name_file), 'rb') as p:
    #     txt = (p.readlines())

    ## print(txt)
    # txtx = reset_eof_of_pdf_return_stream(txt)

    # with open('{}/{}'.format(path, fixed_file), 'wb') as f:
    #     f.writelines(txtx)
      
    # pdf_file = PyPDF2.PdfFileReader('{}/{}'.format(path, fixed_file))
    pdf_file = PyPDF2.PdfFileReader('{}/{}'.format(path, name_file))
    
    num_pages = pdf_file.getNumPages()
    
    if verbose:
        print("Number pages: {}".format(num_pages))
        
    pages = get_pages(pdf_file, num_pages)
    content = extract_text(pages)

    
    return " ".join(content)


path = '/home/asafe/GitHub/Coleta_C01/Para_de_Minas/esic/data/files/'
name_file = '2f37e03c3179bb4f1312f2093f6742af.pdf.pdf'
fixed_file= 'Licitacao_fixed.pdf'
content = main(name_file, fixed_file, path, verbose=True)
content = remove_noise(content)
# print(content)
