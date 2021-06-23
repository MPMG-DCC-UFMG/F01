from bs4 import BeautifulSoup

def search_in_home(home_file, keys):
    html = BeautifulSoup(home_file.read(),  "html.parser" )
    possible_urls = []
    for elem in html.find_all(href=True):
        for s in keys:
            if s in elem.getText():
                possible_urls.append(elem['href'])

    return possible_urls