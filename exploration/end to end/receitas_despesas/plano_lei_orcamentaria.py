from bs4 import BeautifulSoup
import codecs
import constant

items = {
    'PLANO_PLURIANUAL': False,
    'LEI_ORCAMENTARIA': False,
    'LEI_DIRETRIZES': False
}

#Tag item exists
def get_macro(item_text):
    filename = './Governador Valadares/home/home.html'   
    file = codecs.open(filename, 'r', 'utf-8')
    html = BeautifulSoup(file.read(),  "html.parser" )
    return html.find(text = item_text, href=True)

def explain(macro,item_text):
    if(macro is None):
        print("Não foi encontrado no menu principal do portal um link que possua como valor textual alguma das seguintes palavras chave:")
        for fs in item_text:
            print(fs, ' ')
        return  
    
    print("Foi encontrado no menu principal do portal um link que tinha como valor textual:", macro.getText(), "\nLink:", macro['href'])

def predict(href,key):
    if href is not None:
        items[key] = True 

def validate_item(item_text,key):
    macro = get_macro(item_text)
    predict(macro['href'],key)
    explain(macro,item_text)

def main():
    for key in constant.LEIS_ORCAMENTARIAS:
        validate_item(constant.LEIS_ORCAMENTARIAS[key],key)
    print(items)
main()
