import codecs
import constant
from bs4 import BeautifulSoup
import re

# Possui local e instruções para fácil acesso do interessado à comunicação com o município, por via eletrônica ou telefônica 

def search_telephone_number(markup_html):
    text = markup_html.getText()

    pattern = r"\(?(?:3[1234578])\)? ?(?:[2-8]|9[1-9])[0-9]{3}\-?[0-9]{4}"
    # print (re.findall(pattern, text))

    return (bool(re.findall(pattern, text)))

def search_address_tag(markup_html, search):

    for address_tag in markup_html.find_all("address"):
        address_text = address_tag.getText()
        # print(address_text)
    
        for word in search: 
            p = re.compile(f'{word}')

            m = p.findall(address_text)
            # print("M>>>",m)
            if p.findall(address_text): return True

    return False

def search_contact_us():
    pass

def main():
    file = codecs.open('Governador Valadares/home/home.html', 'r', 'utf-8')    
    html = BeautifulSoup(file.read(),  "html.parser" )

    # Search for contact in Home

    # If it has an address tag
    print("search_address_tag: ", search_address_tag(html, constant.CONTACT))

    # If it has an contact number
    print("search_telephone_number: ", search_telephone_number(html))


main()