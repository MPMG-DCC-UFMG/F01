from bs4 import BeautifulSoup
import codecs
import re
import constant
from os import walk
from utils import indexing
from utils import search_path_in_dump


#--------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------Requisitos Exigidos nos sítios eletrônicos--------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------#



# Possibilita a gravação de relatórios em diversos formatos eletrônicos, 
# inclusive abertos e não proprietários (possibilidade de acessar e 
# gravar os relatórios disponibilizados no sítio eletrônico em vários formatos)

def predict_gravar(search_term, keywords, path_base, num_matches = 1,
    job_name = 'index_gv', threshold= 0):

    # _, sorted_result = indexing.request_search(
    #   search_term=search_term, keywords = keywords, num_matches=num_matches, job_name=job_name)
    # path = [i[2] for i in sorted_result]
    # path_html = search_path_in_dump.agg_type(path)["html"]

    result = {
        'n_paginas': 0,
    }

    # for filename in path_html:
    result['n_paginas'] += 1
    print('/home/asafe/GitHub/Coleta_C01/Governador Valadares/concursos_governador_valadares/data/raw_pages/3a0f99fc4af191266e8c81049a1f072b.html')
    
    markup = BeautifulSoup(codecs.open('/home/asafe/GitHub/Coleta_C01/Governador Valadares/concursos_governador_valadares/data/raw_pages/3a0f99fc4af191266e8c81049a1f072b.html', 'r', 'utf-8').read(),  "html.parser" )
    search_keywords_gravar(markup, constant.GRAVAR)

    return False, result

def search_keywords_gravar(markup, constants):
    macro = markup.findAll(href = constants)
    print('macro: ', macro)
    # questions_by_t = set(markup.find_all(text= re.compile(r'([?]+$)')))
    # for a in markup.find_all("a", {'id': re.compile(r'^pergunta')}):
    #     questions_by_t.add(a.getText())
    # return markup.find(text=constants), questions_by_t


def explain_gravar(isvalid, result):
    print(f'Prediction gravação de relatórios: {isvalid}')
    print(f"Foram encontradas pelo menos {result['n_paginas']} com possíbilidade de gravar relatórios")



def predict_requisitos_exigidos_dos_sites():
    # Contém ferramenta de pesquisa de conteúdo que permite o acesso à informação (a ferramenta “lupa” para promover pesquisas no próprio site) 
    # Possibilita a gravação de relatórios em diversos formatos eletrônicos
    # Mantém as informações disponíveis para acesso atualizadas
    # Possui local e instruções para fácil acesso do interessado à comunicação com o município, por via eletrônica ou telefônica 
    # Contém medidas que garantem a acessibilidade de conteúdo para pessoas com deficiência 
    pass


def explain_requisitos_exigidos_dos_sites():
    pass

