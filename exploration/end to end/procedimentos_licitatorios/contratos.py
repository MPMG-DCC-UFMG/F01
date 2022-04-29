from bs4 import BeautifulSoup
import pandas as pd
import codecs
import utilconst.constant as constant
from os import walk

def get_all_filenames_in_dir(dir):
    f = []
    for (dirpath, dirnames, filenames) in walk(dir):
        f.extend(filenames)
        break
    return f

#Tag item exists
def get_macro():
    filename = './Governador Valadares/home/home.html'   
    file = codecs.open(filename, 'r', 'utf-8')
    html = BeautifulSoup(file.read(),  "html.parser" )
    return html.find(text = constant.CONTRATOS, href=True)

#Searches for button for sorting elements
def checks_for_order(html):
    order = html.find(text = constant.ORDENAR)
    return order

#Searches page for table of elements 
def validate_elements(html):
    table = html.find('table')
    return table.find('summary')            

#iterates through all pages calling the function above
def check_for_elements(dir, filenames):
    for f in filenames:
        html = BeautifulSoup(codecs.open(dir + '/' +  f, 'r', 'utf-8').read(),  "html.parser" )
        table = validate_elements(html)
        return table
    return None


def predict(table, order):
    prediction = table.getText() in constant.CONTRATOS and order is not None
    return prediction

def explain(macro, table, order):
    if(macro is None):
        print("Não foi encontrado no menu principal do portal um link que possua como valor textual alguma das seguintes palavras chave:")
        for fs in constant.CONTRATOS:
            print(fs, ' ')
        return 
    
    print("Foi encontrado no menu principal do portal um link que tinha como valor textual:", macro.getText(), "\nLink:", macro['href'])
    if(table is None):    
        print("\nNão foi encontrada nenhuma tabela com alguma  das seguintes palavras chave:")
        for fs in constant.CONTRATOS:
            print(fs, ' ')
        return 

    print("\nNa página direcionada pelo link foi encontrada uma tabela com o seguinte título:", table.getText())    
    if(order is None):
        print("Não é possível organizar os resultados por uma ordem cronológica\n")
        return
    print("É possível organizar os resultados por uma ordem cronológica\n")
     

def main():
    macro = get_macro()
    if(not macro):  
        prediction = False 
    else:
        dir = './Governador Valadares/contratos-aditivos'   
        filenames = get_all_filenames_in_dir(dir)
        base_file = codecs.open(dir + '/' +  filenames[0], 'r', 'utf-8')

        table = check_for_elements(dir, filenames) #If the searched elements are in the page
        order = checks_for_order(BeautifulSoup(base_file.read(),  "html.parser" )) # If elements can be sorted

        prediction = predict(table, order)
    
    print("\nPrediction:", prediction, "\n")
    explain(macro, table, order)

main()