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
    
    return texts


def main(name_file, path, verbose=True):
    
    pdf_file = PyPDF2.PdfFileReader('{}/{}'.format(path, name_file))
    num_pages = pdf_file.getNumPages()
    
    if verbose:
        print("Number pages: {}".format(num_pages))
        
    pages = get_pages(pdf_file, num_pages)
    content = extract_text(pages)
    
    return " ".join(content)


path = '../../../persistence_area'
name_file = 'Relatorio_Anual_de_Prestacao_de_Contas_Municipal_869_Ano_2020.pdf'
content = main(name_file, path, verbose=True)
content = remove_noise(content)
content
