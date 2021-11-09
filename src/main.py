import sys
import pandas as pd
#sys.path.insert(1, './classifiers')

# sys.path.insert(0, '/home/cinthia/F01/src/classifiers')

# from concursos import predict_copia_edital, explain_copia_edital, predict_recursos, explain_recursos, predict_dados_concurso, explain_dados_concurso
# from diaria_viagem import predict_diaria_viagem, explain_diaria_viagem
# from info_institucionais import predict_estrutura_organizacional,explain_estrutura_organizacional,predict_link_legislacao,explain_link_legislacao,predict_unidades_administrativas,explain_unidades_administrativas

from classifiers.acesso_a_informacao import requisitos_sitios
from classifiers.acesso_a_informacao import informacoes
from classifiers.acesso_a_informacao import base_dados
from classifiers.acesso_a_informacao import divulgacao_atendimentos
from classifiers import licitacoes 
import constant

def add_in_dict(output, item, isvalid, result_explain):

    output[item]['predict'] = isvalid
    output[item]['explain'] = result_explain

    return output

def pipeline_informacoes(keywords, path_base, num_matches, job_name):

    output = {'link_portal': {},
              'text_expl': {},
              'legs_federal': {},
              'legs_estadual': {},
              'site_transparencia': {},
              'acesso_ilimitado': {},
              'faq': {},
              'new_predict_text_expl': {},
              }

    # Uberlândia
    # #--- Aba denominada “Transparência” no menu principal do site
    # isvalid, result = informacoes.predict_link_portal(path_base = path_base, num_matches=500,
    #     job_name='index_uberlandia')
    # informacoes.explain_link_portal(isvalid, result)

    # Betim
    # #--- Texto padrão explicativo sobre a Lei de Acesso à Informação
    # isvalid, result = informacoes.predict_text_expl(path_base = path_base, num_matches = 10, job_name='index_betim')
    # informacoes.explain_text_expl(isvalid, result)

    # --- Aba denominada “Transparência” no menu principal do sítio eletrônico
    isvalid, result = informacoes.predict_link_portal(path_base = path_base, job_name=job_name)
    result_explain  = informacoes.explain_link_portal(result, column_name='matches', elemento='link_portal')
    output = add_in_dict(output, 'link_portal', isvalid, result_explain)

    #--- Texto padrão explicativo sobre a Lei de Acesso à Informação
    isvalid, result = informacoes.predict_text_expl(path_base = path_base, job_name=job_name)
    result_explain  = informacoes.explain(result, column_name='matches', elemento='text_expl', verbose=False)
    output = add_in_dict(output, 'text_expl', isvalid, result_explain)

    # Link de acesso à leg federal sobre a transp (Lei nº 12.527/2011)
    isvalid, result = informacoes.predict_legs_federal(path_base = path_base, job_name=job_name)
    result_explain = informacoes.explain_legs_federal(isvalid, result)
    output = add_in_dict(output, 'legs_federal', isvalid, result_explain)

    # Link de acesso à leg sobre a transparência (Decreto Estadual nº 45.969/2012)
    isvalid, result = informacoes.predict_legs_estadual(path_base = path_base, job_name=job_name)
    result_explain = informacoes.explain_legs_estadual(isvalid, result)
    output = add_in_dict(output, 'legs_estadual', isvalid, result_explain)

    # Link de acesso ao site da Transparência (www.transparencia.mg.gov.br)
    isvalid, result = informacoes.predict_site_transparencia(path_base = path_base, job_name=job_name)
    result_explain = informacoes.explain_site_transparencia(isvalid, result)
    output = add_in_dict(output, 'site_transparencia', isvalid, result_explain)

    # Acesso ilimitado a todas as informações públicas do sítio eletrônico
    isvalid, result = informacoes.predict_acesso_ilimitado(path_base = path_base, job_name=job_name)
    result_explain = informacoes.explain_acesso_ilimitado(isvalid, result, column_name='matches', elemento='login')
    output = add_in_dict(output, 'acesso_ilimitado', isvalid, result_explain)

    # Link de respostas a perguntas mais frequentes da sociedade.
    isvalid, result = informacoes.predict_faq(path_base = path_base, job_name=job_name)
    result_explain = informacoes.explain_faq(isvalid, result)
    output = add_in_dict(output, 'faq', isvalid, result_explain)

    return output

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

def pipeline_base_dados(keywords, path_base, num_matches, job_name, verbose=False):

    output = {'relação_das_bases': {},
              }

    # Publica na internete relação das bases de dados abertos do município ou do estado
    isvalid, result = base_dados.predict_bases_de_dados_abertos(path_base = path_base, job_name=job_name)
    result_explain = base_dados.explain_bases_de_dados_abertos(isvalid, result)

    output = add_in_dict(output, 'relação_das_bases', isvalid, result_explain)

    return output

def pipeline_divulgacao_atendimentos(keywords, path_base, num_matches, job_name, verbose=False):

    output = {'pedidos_recebidos': {},
              'pedidos_atendidos': {},
              'pedidos_indeferidos': {},
              }

    # Quantidade de pedidos recebidos
    isvalid, result = divulgacao_atendimentos.predict_pedidos_recebidos(path_base = path_base, job_name=job_name)
    result_explain = divulgacao_atendimentos.explain(result, column_name='matches', elemento='pedidos_recebidos', verbose=False)

    output = add_in_dict(output, 'pedidos_recebidos', isvalid, result_explain)

    # Quantidade e/ou percentual de pedidos atendidos
    isvalid, result = divulgacao_atendimentos.predict_pedidos_atendidos(path_base = path_base, job_name=job_name)
    result_explain = divulgacao_atendimentos.explain(result, column_name='matches', elemento='pedidos_atendidos', verbose=False)

    output = add_in_dict(output, 'pedidos_atendidos', isvalid, result_explain)

    # Quantidade e/ou percentual de pedidos indeferidos
    isvalid, result = divulgacao_atendimentos.predict_pedidos_indeferidos(path_base = path_base, job_name=job_name)
    result_explain = divulgacao_atendimentos.explain(result, column_name='matches', elemento='pedidos_indeferidos', verbose=False)

    output = add_in_dict(output, 'pedidos_indeferidos', isvalid, result_explain)

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

    # output_informacoes = pipeline_informacoes(
    #     keywords, path_base, num_matches, job_name)
    # output_requisitos_sitios = pipeline_requisitos_sitios(
    #     keywords, path_base, num_matches, job_name)
    output_licitacoes = pipeline_licitacoes(
        keywords, path_base, pattern, num_matches, job_name, tags)


    output = {
                # 'informacoes': output_informacoes, 
                # 'requisitos_sitios': output_requisitos_sitios,
                'licitacoes': output_licitacoes}

    return output


# path_base = "/home/cinthia/F01/data"
path_base = "/home/asafe"
num_matches = 10
job_name = 'index_para_de_minas'
keywords = constant.keywords
pattern = ''
tags = ''

# main()

# result = pipeline_informacoes(keywords, path_base, num_matches, job_name)
# df = pd.DataFrame(result).T
# df.to_csv("result_informacoes.csv", index=False)

# result = pipeline_requisitos_sitios(keywords, path_base, num_matches, job_name)
# df = pd.DataFrame(result).T
# df.to_csv("result.csv", index=False)
# print(pd.DataFrame(result).T)

# result = pipeline_base_dados(keywords, path_base, num_matches, job_name)
# df = pd.DataFrame(result).T
# df.to_csv("result_base_dados.csv", index=False)


result = pipeline_divulgacao_atendimentos(keywords, path_base, num_matches, job_name)
df = pd.DataFrame(result).T
df.to_csv("result_divulgacao_atendimentos.csv", index=False)

