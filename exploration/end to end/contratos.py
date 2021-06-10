from bs4 import BeautifulSoup
import pandas as pd
import codecs
import constant
from os import walk

def get_all_filenames_in_dir(dir):
    f = []
    for (dirpath, dirnames, filenames) in walk(dir):
        f.extend(filenames)
        break
    return f

#Still no way to link btn links to folders 
def get_item_page(link):
   #To-do
   return './Governador Valadares/contratos-aditivos'

#Tag item exists
def get_macro():
    filename = './Governador Valadares/home/home.html'   
    file = codecs.open(filename, 'r', 'utf-8')
    html = BeautifulSoup(file.read(),  "html.parser" )
    return html.find(text = constant.CONTRATOS, href=True)['href']

#Searches for button for sorting elements
def checks_for_order(html):
    order = html.find(text = constant.ORDENAR)
    return order is not None

#Searches page for table of elements 
def validate_elements(html):
    table = html.find('table')
    if table.find('summary'):
        if table.find('summary').getText() in constant.CONTRATOS:
            return table     
    return False

#iterates through all pages calling the function above
def searches_for_elements(dir, filenames):
    for f in filenames:
        html = BeautifulSoup(codecs.open(dir + '/' +  f, 'r', 'utf-8').read(),  "html.parser" )
        elements = validate_elements(html)
        if elements: return True
    return False

def main():
    macro = get_macro()
    if(not macro):  return 

    dir = get_item_page(macro)   
    filenames = get_all_filenames_in_dir(dir)
    base_file = codecs.open(dir + '/' +  filenames[0], 'r', 'utf-8')

    elements = searches_for_elements(dir, filenames) #If the searched elements are in the page
    order = checks_for_order(BeautifulSoup(base_file.read(),  "html.parser" )) # If elements can be sorted

    print(elements, order)
main()