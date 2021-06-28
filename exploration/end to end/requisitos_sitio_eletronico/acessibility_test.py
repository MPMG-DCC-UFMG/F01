from bs4 import BeautifulSoup
# from py_w3c.validators.html.validator import HTMLValidator
# from joblib import Memory
import exceptions
import codecs
import time

# location = "./cachedir"
# memory = Memory(location, verbose=0)

acessibilidade = {
    'alt_att_on_img': {'value': True, 'expĺain': "Todas as imagens tem descrição: "},
    'tag_h1': {'value': True, 'expĺain': "Existe uma tag H1: "},
    'ordem': {'value': True, 'expĺain': "Hierarquia de tags H correta (não tem um H1 depois de um H3 por exemplo): "},
}

def check_alt_att_on_img(html_recebido: str):
    exceptions_list = []
    soup = BeautifulSoup(html_recebido, "html.parser")
    for tag in soup.find_all("img"):
        if not tag.has_attr("alt"):
            acessibilidade["alt_att_on_img"]["value"] = False
            exceptions_list.append(
                exceptions.AcessibilityException(
                    "AcessibilityException",
                    tag,
                    "Missing alt atribute on tag image",
                    tag.sourceline,
                    tag.sourcepos,
                )
            )
        elif tag["alt"] == "":
            acessibilidade["alt_att_on_img"]["value"] = False
            exceptions_list.append(
                exceptions.AcessibilityException(
                    "AcessibilityException",
                    tag,
                    "Empty alt description",
                    tag.sourceline,
                    tag.sourcepos,
                )
            )
    return exceptions_list


def check_for_h1(html_recebido: str):
    exceptions_list = []
    soup = BeautifulSoup(html_recebido, "html.parser")
    tag = soup.find("h1")
    if tag == None:
        acessibilidade["tag_h1"]["value"] = False
        exceptions_list.append(
            exceptions.AcessibilityException(
                "AcessibilityException", "", "Missing header tag H1 on document", "", ""
            )
        )
    return exceptions_list


def check_hs_hierarchy(html_recebido: str):
    exceptions_list = []

    head_tags = {
        "h1": False,
        "h2": False,
        "h3": False,
        "h4": False,
        "h5": False,
        "h6": False,
    }
    existing_tags = []

    soup = BeautifulSoup(html_recebido, "html.parser")
    for tag in soup.find_all(True):
        if tag.name in head_tags and not any(
            tag.name in name for name in existing_tags
        ):
            existing_tags.append((tag.name, tag))

    for name, code_fragment in existing_tags:
        head_tags[name] = True
        for value in head_tags:
            if value != name:
                if head_tags[value] == False:
                    acessibilidade["ordem"]["value"] = False
                    exceptions_list.append(
                        exceptions.AcessibilityException(
                            "AcessibilityException",
                            code_fragment,
                            "Suspected hierarchical order, consider reviewing it, Tag {} appeared first even without the existence of the {} tag".format(
                                name, value
                            ),
                            code_fragment.sourceline,
                            code_fragment.sourcepos,
                        )
                    )
            else:
                break

    return exceptions_list


# def validade_html(html_recebido: str):
#     vld = HTMLValidator()
#     vld.validate_fragment(str(html_recebido))
#     exceptions_list = []

#     for error in vld.errors:
#         exceptions_list.append(
#             exceptions.AcessibilityException(
#                 "StaticHTMLValidation",
#                 error["extract"].replace("\n", ""),
#                 error["message"],
#                 error["hiliteStart"],
#                 error["hiliteLength"],
#             )
#         )
#     return exceptions_list


def map_functions():
    # validade_html_cached = memory.cache(validade_html)
    functions = {
        "alt_att_check": check_alt_att_on_img,
        "contains_h1": check_for_h1,
        "headers_tag_hierarchy": check_hs_hierarchy,
        # "static_validation_html": validade_html_cached,
    }
    return functions


def check_accessibility(html_recebido: str, exclude=()):
    functions_to_check = [
        fn for name, fn in map_functions().items() if name not in exclude
    ]
    exceptions = []
    for func in functions_to_check:
        exceptions.extend(func(html_recebido))
    if exceptions:
        return exceptions


def predict_acessibilidade(html):

    macro = check_accessibility(html)

    if(macro is None):
        return True
    else: return False

def explain(macro, exceptions):

    print("\n", "Explain: predict = ", macro,"\n")

    if(macro is None):
        print("Todos os seguintes itens foram checados: \n")
        for item in acessibilidade:
            print(acessibilidade[item]["expĺain"] + ": ",acessibilidade[item]["value"], "\n")

    else:
        print("Todos os seguintes itens foram checados: \n")
        for item in acessibilidade:
            print(acessibilidade[item]["expĺain"] + ": ",acessibilidade[item]["value"], "\n")


def main():
    file = codecs.open('homeSite.html', 'r', 'utf-8')    
    html = file.read()
    macro = predict_acessibilidade(html)
    exceptions = check_accessibility(html)
    explain(macro, exceptions)


main()