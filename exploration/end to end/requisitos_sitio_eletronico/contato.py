import codecs
import constant
from bs4 import BeautifulSoup
import re

# Possui local e instruções para fácil acesso do interessado à comunicação com o município, por via eletrônica ou telefônica 

contato = {
    'search_address_tag': False,
    'search_telephone_number': False,
}


def search_telephone_number(markup_html):
    text = markup_html.getText()

    pattern = r"\(?(?:3[1234578])\)? ?(?:[2-8]|9[1-9])[0-9]{3}\-?[0-9]{4}"
    # print (re.findall(pattern, text))

    return (re.findall(pattern, text))

def search_address_tag(markup_html, search):

    for address_tag in markup_html.find_all("address"):
        address_text = address_tag.getText()
        # print(address_text)
    
        for word in search: 
            p = re.compile(f'{word}')

            m = p.findall(address_text)
            # print("M>>>",m)
            if p.findall(address_text): return m

    return False

def search_contact_us():
    pass

def explain():
    print("\n") 
    if (contato["search_telephone_number"]):
        print("Foi encontrado o número de telefone: ", contato["search_telephone_number"])
    else: 
        print("Não foi encontrado um número de telefone")

    if (contato["search_address_tag"]):
        print("Foi encontrada a seguinte referência em uma tag <address>: ", contato["search_address_tag"])
    else: 
        print("Não foi encontrado informações na tag <address> um valor textual das seguintes palavras chave")
    print("\n")

def predict():
    for key in contato.keys():
        if contato[key]: return True
    return False


def main():
    file = codecs.open('Governador Valadares/home/home.html', 'r', 'utf-8')    
    html = BeautifulSoup(file.read(),  "html.parser" )

    # Search for contact in Home

    # If it has an address tag

    contato["search_address_tag"] = search_address_tag(html, constant.CONTACT)
    print("search_address_tag: ", search_address_tag(html, constant.CONTACT))

    # If it has an contact number
    contato["search_telephone_number"] = search_telephone_number(html)
    print("search_telephone_number: ", search_telephone_number(html))

    print(predict())

    explain()


main()