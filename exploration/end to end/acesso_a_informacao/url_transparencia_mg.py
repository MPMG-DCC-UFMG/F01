from bs4 import BeautifulSoup
import codecs
import utilconst.constant as constant

items = {
    'URL_TRANSPARENCIA_MG' : False
}

#Tag item exists
def get_macro(item_text):
    filename = './Governador Valadares/home/home.html'   
    file = codecs.open(filename, 'r', 'utf-8')
    html = BeautifulSoup(file.read(),  "html.parser" )
    return html.find(href = item_text)

def explain(macro,item_text):
    if(macro is None):
        print("Não foi encontrado no menu principal do portal o link:\n",item_text)
    
    print("Foi encontrado no menu principal do portal o link :", macro['href'])

def predict(macro):
    if macro is not None:
        items['URL_TRANSPARENCIA_MG'] = True

def main():
    item_text = constant.URL_TRANSPARENCIA_MG
    macro = get_macro(item_text)
    predict(macro)
    explain(macro,item_text)
    print(items)
main()
