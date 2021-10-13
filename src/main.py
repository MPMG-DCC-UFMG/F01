import sys
import pandas as pd
#sys.path.insert(1, './classifiers')

sys.path.insert(0, '/home/cinthia/F01/src/classifiers')

# from concursos import predict_copia_edital, explain_copia_edital, predict_recursos, explain_recursos, predict_dados_concurso, explain_dados_concurso
# from diaria_viagem import predict_diaria_viagem, explain_diaria_viagem
# from info_institucionais import predict_estrutura_organizacional,explain_estrutura_organizacional,predict_link_legislacao,explain_link_legislacao,predict_unidades_administrativas,explain_unidades_administrativas
<<<<<<< HEAD
#from acesso_a_informacao.informacoes import predict_legs_federal, explain_legs_federal
#from acesso_a_informacao.informacoes import predict_text_expl, explain_text_expl
#from acesso_a_informacao.informacoes import predict_faq, explain_faq
from acesso_a_informacao import requisitos_sitios
=======

from acesso_a_informacao.informacoes import predict_link_portal, explain_link_portal
from acesso_a_informacao.informacoes import predict_text_expl, explain_text_expl

from acesso_a_informacao.informacoes import predict_legs_federal, explain_legs_federal
from acesso_a_informacao.informacoes import predict_legs_estadual, explain_legs_estadual
from acesso_a_informacao.informacoes import predict_site_transparencia, explain_site_transparencia
from acesso_a_informacao.informacoes import predict_acesso_ilimitado, explain_acesso_ilimitado
from acesso_a_informacao.informacoes import predict_faq, explain_faq



import licitacoes 
import constant

def add_in_dict(output, item, isvalid, result_explain):


    output[item]['predict'] = isvalid
    output[item]['explain'] = result_explain

    return output

"""def pipeline_informacoes(keywords, path_base, pattern, num_matches, job_name, verbose=False):

    output = {}

    # Acesso à informação
    
    # Link de acesso à legislação federal sobre a transparência (Lei nº 12.527/2011 e eventual legislação superveniente)
    search_term='Acesso a informao'
    keywords=['http://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12527.htm']
    isvalid, result = predict_legs_federal(
        search_term, keywords, path_base, num_matches=40,
        job_name='index_gv', threshold = 0)
    explain_legs_federal(result)

    # Texto padrão explicativo sobre a Lei de Acesso à Informação
    search_term='Lei de acesso'
    keywords=['LAI', 'Lei de acesso à informação']
    isvalid, result = predict_text_expl(
            search_term, keywords, path_base, num_matches=30,
            job_name='index_gv', threshold = 0)
    explain_text_expl(isvalid, result)

    # Link de respostas a perguntas mais frequentes da sociedade.
    search_term='Perguntas Frequentes'
    keywords=['FAQ', 'Perguntas', 'Respostas']
    isvalid, result = requisitos_sitios.predict_faq(
        search_term, keywords, path_base, num_matches=30,
        job_name='index_gv', threshold = 0)
    explain_faq(isvalid, result)

    
    #local onde está o dump
    path_base = "/home/asafe"
    #path_base = "/home/cinthia/MPMG/persistence_area"
    # path_base = "C:/Users/ritar"
    # path_base = "C:/Users/pedro"

# -----------------------------------------

    # Uberlândia

    #-------------------------------INFORMAÇÃO-------------------------------------

    # #--- Aba denominada “Transparência” no menu principal do site
    # isvalid, result = predict_link_portal(path_base = path_base, num_matches=500,
    #     job_name='index_uberlandia')
    # explain_link_portal(isvalid, result)

    #--- Texto padrão explicativo sobre a Lei de Acesso à Informação
    isvalid, result = predict_text_expl(path_base = path_base, job_name='index_uberlandia')
    explain_text_expl(isvalid, result)

    # #--- Link de acesso à legislação federal (Lei nº 12.527/2011)
    # isvalid, result = predict_legs_federal(path_base = path_base, job_name='index_uberlandia')
    # explain_legs_federal(isvalid, result)

    # #--- Link de acesso à legislação (Decreto Estadual nº 45.969/2012)
    # isvalid, result = predict_legs_estadual(path_base = path_base, job_name='index_uberlandia')
    # explain_legs_estadual(isvalid, result)

    # #--- Link de acesso www.transparencia.mg.gov.br
    # isvalid, result = predict_site_transparencia(path_base=path_base, num_matches=40, job_name='index_uberlandia')
    # explain_site_transparencia(isvalid, result)

    # #-- Acesso ilimitado a todas as informações públicas disponibilizadas no sítio eletrônico
    # isvalid, result = predict_acesso_ilimitado(path_base=path_base, job_name='index_uberlandia')
    # explain_acesso_ilimitado(isvalid, result)

    # #--- FAQ
    # isvalid, result = predict_faq(path_base=path_base, job_name='index_uberlandia')
    # explain_faq(isvalid, result)

# -----------------------------------------

    # Para de Minas

    # # --- Aba denominada “Transparência” no menu principal do sítio eletrônico
    # isvalid, result = predict_link_portal(path_base = path_base, job_name='index_para_de_minas')
    # explain_link_portal(isvalid, result)

    # #--- Texto padrão explicativo sobre a Lei de Acesso à Informação
    # isvalid, result = predict_text_expl(path_base = path_base, job_name='index_para_de_minas')
    # explain_text_expl(isvalid, result)

    # #--- Link de acesso à legislação federal (Lei nº 12.527/2011)
    # isvalid, result = predict_legs_federal(path_base = path_base, job_name='index_para_de_minas')
    # explain_legs_federal(isvalid, result)

    # #--- Link de acesso à legislação (Decreto Estadual nº 45.969/2012)
    # isvalid, result = predict_legs_estadual(path_base = path_base, job_name='index_para_de_minas')
    # explain_legs_estadual(isvalid, result)

    # #--- Link de acesso www.transparencia.mg.gov.br
    # isvalid, result = predict_site_transparencia(path_base=path_base, num_matches=40, job_name='index_para_de_minas')
    # explain_site_transparencia(isvalid, result)

    # #-- Acesso ilimitado a todas as informações públicas disponibilizadas no sítio eletrônico
    # isvalid, result = predict_acesso_ilimitado(path_base=path_base, job_name='index_para_de_minas')
    # explain_acesso_ilimitado(isvalid, result)

    # #--- FAQ
    # isvalid, result = predict_faq(path_base=path_base, job_name='index_para_de_minas')
    # explain_faq(isvalid, result)


    return output"""



def pipeline_requisitos_sitios(keywords, path_base, num_matches, job_name, verbose=False):

    output = {'search_engine': {},
              'export_reports': {},
              'update_infos': {},
              'accessibility': {},
              'address': {}}

    #Contém ferramenta de pesquisa
    search_term = keywords['search_engine']['search_term']
    keywords_to_search = keywords['search_engine']['keywords']

    isvalid, result = requisitos_sitios.predict_search_engine(
        search_term=search_term, keywords=keywords_to_search,
        job_name=job_name, path_base=path_base,
            verbose=verbose)
    result_explain = requisitos_sitios.explain(
        result, column_name='matches', elemento='Possui ferramenta de pesquisa', verbose=verbose)

    output = add_in_dict(output, 'search_engine', isvalid, result_explain)

    # Possibilita gravação de relatórios
    search_term = keywords['export_reports']['search_term']
    keywords_to_search = keywords['export_reports']['keywords']

    isvalid, result = requisitos_sitios.predict_export_reports(
        search_term=search_term, keywords=keywords_to_search,
        job_name=job_name, path_base=path_base, 
            verbose=verbose)
    result_explain  = requisitos_sitios.explain(
        result, column_name='matches', elemento='Permite exportar relatórios', verbose=verbose)

    output = add_in_dict(output, 'export_reports', isvalid, result_explain)

    # Mantém as informações atualizadas
    search_term = keywords['update_infos']['search_term']
    keywords_to_search = keywords['update_infos']['keywords']

    isvalid, result = requisitos_sitios.predict_update_infos(
        search_term=search_term, keywords=keywords_to_search,
        job_name=job_name, path_base=path_base, 
        verbose=verbose)
    result_explain = requisitos_sitios.explain(
        result, column_name='matches', elemento='Mantém as informações atualizadas', verbose=verbose)

    output = add_in_dict(output, 'update_infos', isvalid, result_explain)

    # Possui mecanismos de acessibilidade
    search_term = keywords['accessibility']['search_term']
    keywords_to_search = keywords['accessibility']['keywords']

    isvalid, result = requisitos_sitios.predict_accessibility (
        search_term=search_term, keywords=keywords_to_search,
        job_name=job_name, path_base=path_base, 
        verbose=verbose)
    result_explain = requisitos_sitios.explain(
        result, column_name='matches', elemento='Possui mecanismos de acessibilidade', verbose=verbose)

    output = add_in_dict(output, 'accessibility', isvalid, result_explain)

    # Possui local e instruções para fácil acesso do interessado à comunicação com o município
    search_term = keywords['address']['search_term']
    keywords_to_search = keywords['address']['keywords']

    isvalid, result = requisitos_sitios.predict_address(
        search_term=search_term, keywords=keywords_to_search,
        job_name=job_name, path_base=path_base, 
            verbose=verbose)
    result_explain = requisitos_sitios.explain(
        result, column_name='matches', elemento='Disponibiliza Endereço', verbose=verbose)

    result.to_csv("test.csv", index=False)

    output = add_in_dict(output, 'address', isvalid, result_explain)

    return output



def pipeline_licitacoes(keywords, path_base, pattern, num_matches, job_name, tags, verbose=False):

    search_term=keywords['proc_lic']['search_term']
    keywords_to_search = keywords['proc_lic']['keywords']
    itens=keywords['proc_lic']['itens']

    output = {'proc_lic': {},
            'inexigibilidade': {},
            'resultado': {},
            'dispensa': {},
            'editais': {},
            'busca': {}}

    # Procedimentos licitatórios
    isvalid, result = licitacoes.predict_proc_lic(
        search_term=search_term, keywords_search=keywords, keywords_check=itens, 
        path_base=path_base, num_matches=num_matches,
        filter_word='licitacoes', job_name=job_name, threshold = 0)

    for i in range(len(itens)):
        print("Predict - Procedimentos Licitatórios - {}: {}".format(itens[i], isvalid[i]))
        result_explain = licitacoes.explain(result['proc_lic'], itens[i])

    output = add_in_dict(output, 'proc_lic', isvalid, result_explain)

    # Procedimentos de Inexigibilidade
    isvalid, result = licitacoes. predict_inexigibilidade(
        search_term=search_term, keywords=keywords_to_search,
        path_base=path_base, num_matches=num_matches,
        filter_word='licitacoes', job_name='index_gv', threshold=0)

    result_explain=licitacoes.explain(result, 'inexigibilidade')

    output = add_in_dict(output, 'inexigibilidade', isvalid, result_explain)

    #Resultado
    isvalid, result = licitacoes.predict_resultado(
        search_term=search_term, keywords_search=keywords_to_search, path_base=path_base, num_matches=40,
        filter_word='licitacoes', job_name='index_gv', threshold=0)
    
    result_explain=licitacoes.explain(result, 'resultado')

    output = add_in_dict(output, 'resultado', isvalid, result_explain)

    #Dispensa
    isvalid, result = licitacoes.predict_dispensa(
        search_term=search_term, keywords_search=keywords_to_search,
        path_base=path_base, num_matches=num_matches,
        filter_word='licitacoes', job_name='index_gv', threshold=0)

    result_explain=licitacoes.explain(result, 'dispensa')

    output = add_in_dict(output, 'dispensa', isvalid, result_explain)

    # Disponibilização de Editais
    isvalid, result = licitacoes.predict_editais(
            search_term=search_term, keywords_search=keywords_to_search,
            path_base=path_base, num_matches=num_matches,
            filter_word='licitacoes', job_name='index_gv', threshold=0)

    result_explain=licitacoes.explain(result, 'editais')

    output = add_in_dict(output, 'editais', isvalid, result_explain)

    # Permite Busca
    isvalid, result = licitacoes.predict_busca(
        search_term=search_term, keywords_search=keywords_to_search,
        path_base=path_base, num_matches=num_matches,
        filter_word='licitacoes', job_name='index_gv', threshold=0)

    result_explain=licitacoes.explain(result, 'busca')

    output = add_in_dict(output, 'busca', isvalid, result_explain)

    return output


def main():

    output_informacoes = pipeline_informacoes(
        keywords, path_base, pattern, num_matches, job_name)
    output_requisitos_sitios = pipeline_requisitos_sitios(
        keywords, path_base, pattern, num_matches, job_name)
    output_licitacoes = pipeline_licitacoes(
        keywords, path_base, pattern, num_matches, job_name)


    output = {'informacoes': output_informacoes, 
              'requisitos_sitios':output_requisitos_sitios,
              'licitacoes': output_licitacoes}

    return output


path_base = "/home/cinthia/F01/data"
num_matches = 10
job_name='index_uberlandia'
keywords = constant.keywords


result = pipeline_requisitos_sitios(keywords, path_base, num_matches, job_name)

df = pd.DataFrame(result).T
df.to_csv("result.csv", index=False)
print(pd.DataFrame(result).T)
