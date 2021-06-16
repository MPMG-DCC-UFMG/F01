from bs4 import BeautifulSoup
import codecs
import re
import constant

items = {
    'URL_PORTAL' : False,
    'ABA_NO_MENU' : False
}

#Tag item exists
def get_macro(item_text):
    filename = './homeSite.html'   
    file = codecs.open(filename, 'r', 'utf-8')
    html = BeautifulSoup(file.read(),  "html.parser" )

    macro = html.findAll(href = item_text) 

    return macro

def predict(macro):

    if macro is not None:
        items['URL_PORTAL'] = True

    tags_a = macro

    for tag_a in tags_a:

        tag_parent = tag_a.parent
        tag_grandparent = tag_parent.parent
        
        if tag_grandparent.find(class_= re.compile("(?:.*sidebar.*|.*navbar.*|.*menu.*)")):
            items['ABA_NO_MENU'] = True

        if tag_grandparent.find(id= re.compile("(?:.*sidebar.*|.*navbar.*|.*menu.*)")):
            items['ABA_NO_MENU'] = True


def explain(items_explain):
    if(items['URL_PORTAL']):
        print("Link para o portal da transparencia encontrado no site\n")  

        if(items['ABA_NO_MENU']):
            print("Link foi encontrado no menu")
        else:
            print("Link não foi encontrado no menu")
    
    else:
        print("Link para o portal da transparencia não foi encontrado no site\n")  
    


def main():
    item_text = constant.ABA_TRANSPARENCIA
    macro = get_macro(item_text)
    predict(macro)
    explain(items)
    print(items)

main()
