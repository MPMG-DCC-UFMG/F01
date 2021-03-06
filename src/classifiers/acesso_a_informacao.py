from bs4 import BeautifulSoup
import codecs
import re
import constant
from os import walk

#--------------------------------------------------------- Acesso à Informações ----------------------------------------------------#


#-------- Aba denominada “Transparência” no menu principal
def search_keywords_linkportal(markup, constants):
    macro = markup.findAll(href = constants) 
    return macro

def predict_link_portal():
    filename = '../../Governador Valadares/homeSite.html'   
    file = codecs.open(filename, 'r', 'utf-8')
    markup = BeautifulSoup(file.read(),  "html.parser" )
    macro = search_keywords_linkportal(markup, constant.ABA_TRANSPARENCIA)

    link_portal = {
    'URL_PORTAL' : False,
    'ABA_NO_MENU' : False
    }

    if macro is not None:
        link_portal['URL_PORTAL'] = True

    tags_a = macro
    for tag_a in tags_a:
        tag_parent = tag_a.parent
        tag_grandparent = tag_parent.parent
        if tag_grandparent.find(class_= re.compile("(?:.*sidebar.*|.*navbar.*|.*menu.*)")):
            link_portal['ABA_NO_MENU'] = True
        if tag_grandparent.find(id= re.compile("(?:.*sidebar.*|.*navbar.*|.*menu.*)")):
            link_portal['ABA_NO_MENU'] = True

    classifier = link_portal['ABA_NO_MENU'] is not None and link_portal['ABA_NO_MENU'] is not None
    print("Prediction aba denominada “Transparência” no menu principal:", classifier)

    return link_portal

def explain_link_portal(link_portal):

    if(link_portal['URL_PORTAL']):
        print("Link para o portal da transparencia encontrado no site")  
        if(link_portal['ABA_NO_MENU']):
            print("\t O link foi encontrado no menu")
        else:
            print("\t O link não foi encontrado no menu")
    
    else:
        print("Link para o portal da transparencia não foi encontrado no site\n")  
# -------------------------------------------------------------------------------------


# Texto padrão explicativo sobre a Lei de Acesso à Informação
def search_keywords_text_expl(markup, constants):
    pass
def predict_text_expl():
    pass
def explain_text_expl():
    pass

# Link de acesso à legislação federal sobre a transparência (Lei nº 12.527/2011 e eventual legislação superveniente)
def search_keywords_legs_federal(markup, constants):
    pass
def predict_legs_federal():
    pass
def explain_legs_federal():
    pass

# Link de acesso à legislação Estadual sobre a transparência (Decreto Estadual nº 45.969/2012 e eventual legislação superveniente)
def search_keywords_legs_estadual(markup, constants):
    pass
def predict_legs_estadual():
    pass
def explain_legs_estadual():
    pass


# Link de acesso ao site da Transparência (www.transparencia.mg.gov.br)

def search_keywords_site_transparencia(markup, constants):
    macro = markup.find(href = constants)
    return macro

def predict_site_transparencia():

    filename = '../../Governador Valadares/home/home.html'   
    file = codecs.open(filename, 'r', 'utf-8')
    markup = BeautifulSoup(file.read(),  "html.parser" )

    macro = search_keywords_site_transparencia(markup, constant.URL_TRANSPARENCIA_MG)

    site_transparencia_dict = {
    'URL_TRANSPARENCIA_MG' : False,
    }

    if macro is not None:
        site_transparencia_dict['URL_TRANSPARENCIA_MG'] = True

    return site_transparencia_dict

def explain_site_transparencia(site_transparencia_dict):

    if(site_transparencia_dict['URL_TRANSPARENCIA_MG'] is False):
        print("Não foi encontrado no menu principal do portal o link:\n", constant.URL_TRANSPARENCIA_MG)
    
    else:
        print("Foi encontrado no menu principal do portal o link :", constant.URL_TRANSPARENCIA_MG)

# --------------------------------------------------------------------------------

# Acesso ilimitado a todas as informações públicas do sítio eletrônico: o acesso sem cadastro ou ao fornecimento de dados pessoais
def search_keywords_acesso_ilimitado(markup, constants):
    pass
def predict_acesso_ilimitado():
    pass
def explain_acesso_ilimitado():
    pass


# Link de respostas a perguntas mais frequentes da sociedade.
def search_keywords_faq(markup, constants):
    questions_by_t = set(markup.find_all(text= re.compile(r'([?]+$)')))
    for a in markup.find_all("a", {'id': re.compile(r'^pergunta')}):
        questions_by_t.add(a.getText())
    return markup.find(text=constants), questions_by_t

def predict_faq():
    filename = '../../Governador Valadares/faq/perguntas_frequentes.html'
    markup = BeautifulSoup(codecs.open(filename, 'r', 'utf-8').read(),  "html.parser" )
    title, questions = search_keywords_faq(markup, constant.FAQ_SEARCH)
    classifier = title is not None and questions is not None
    print("\nPrediction Perguntas Frequentes:", classifier)
    ans = {
        'title': title,
        'questions': questions,
        'classifier': classifier 
    }
    return ans

def explain_faq(faq_dict):
    if(faq_dict['classifier']):    
        print("Na página direcionada pelo link foi encontrado o seguinte título:", faq_dict['title'])    
        print("Foram encontradas", len(faq_dict['questions']), "perguntas na página\n")
        for q in faq_dict['questions']:
            print(q)
    elif faq_dict['title'] is None:     
        print("\nNenhuma das palavras chave a seguir foram encontradas na página direcionada pelo link:")
        for fs in constant.FAQ_SEARCH:
            print(fs, ' ')
        



# --------------------------------------------------------------------------------------
# ------------------------------Acesso à Informações------------------------------------
# --------------------------------------------------------------------------------------


def predict_informacoes():

    print("\n -- Prediction Acesso a Informação:  ---- \n")

    link_portal_dict = predict_link_portal()

    # text_expl_dict = predict_text_expl()

    # legs_federal_dict = predict_legs_federal()

    # legs_estadual_dict = predict_legs_estadual()

    site_transparencia_dict =  predict_site_transparencia()

    # acesso_ilimitado_dict = predict_acesso_ilimitado()

    faq_dict = predict_faq()


    informacoes_dict = { 'link_portal_dict': link_portal_dict, 
                        'faq_dict': faq_dict ,
                        'site_transparencia_dict' : site_transparencia_dict,
                        }

    return informacoes_dict


def explain_informacoes(informacoes_dict):

    print("\n --- Explain Acesso a Informação:  ---- \n")


    print("\n - Explain aba denominada transparencia no menu principal: - \n")
    link_portal_dict = informacoes_dict['link_portal_dict']
    explain_link_portal(link_portal_dict)

    print("\n - Explain Perguntas Frequentes: - \n")
    faq_dict = informacoes_dict['faq_dict']
    explain_faq(faq_dict)

    print("\n - Link de acesso ao site da Transparência (www.transparencia.mg.gov.br): - \n")
    site_transparencia_dict = informacoes_dict['site_transparencia_dict']
    explain_site_transparencia(site_transparencia_dict)




# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------




#------------------------------------------ Requisitos Exigidos nos sítios eletrônicos----------------------------------------#


def predict_requisitos_exigidos_dos_sites():
    # Contém ferramenta de pesquisa de conteúdo (“lupa”)
    # Mantém as informações disponíveis para acesso atualizadas
    # Possui local e instruções para fácil acesso do interessado à comunicação com o município, por via eletrônica ou telefônica 
    # Contém medidas que garantem a acessibilidade de conteúdo para pessoas com deficiência 
    pass


def explain_requisitos_exigidos_dos_sites():
    pass



# --------------------------------------------------- Bases de dados abertos --------------------------------------------------#


def predict_bases_de_dados_aberta():
    # Publica na internete relação das bases de dados abertos do município ou do estado
    pass






# -------------------------------------- Relatório estatístico (Divulgação de relatório de atendimentos) -------------------------#


def predict_relatorio_estatistico():
    # Quantidade de pedidos recebidos
    # Quantidade e/ou percentual de pedidos atendidos
    # Quantidade e/ou percentual de pedidos indeferidos
    pass

def explain_relatorio_estatistico():
    pass