import itertools

def get_tags_id (soup):

    #Get all tags id and return a list with all ids
    tags_id = [tag.get('id') for tag in soup.find_all() if tag.get('id') != None]

    return tags_id

def get_tags_class (soup):

    #Get all tags class and return a list with all class
    tags_class =  [tag.get('class') for tag in soup.find_all() if tag.get('class') != None]
    tags_class = list(itertools.chain(*tags_class))
    
    return tags_class

def search_tags_address(tags):

    address = [i for i in tags if ("endereco" in i) or ("address" in i)]

    return address