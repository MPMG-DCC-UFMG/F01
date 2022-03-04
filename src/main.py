import os
from utils.indexing import remove_index
import json
import pandas as pd
import sys

from utils import indexing
from utils import path_functions
from utilconst.constant_pt import municipios_PT
from utilconst.constant_pt import keywords_template

# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument("job")
# args = parser.parse_args()
#sys.path.insert(1, './classifiers')

# sys.path.insert(0, '/home/cinthia/F01/src/classifiers')

# from concursos import predict_copia_edital, explain_copia_edital, predict_recursos, explain_recursos, predict_dados_concurso, explain_dados_concurso
# from diaria_viagem import predict_diaria_viagem, explain_diaria_viagem
# from info_institucionais import predict_estrutura_organizacional,explain_estrutura_organizacional,predict_link_legislacao,explain_link_legislacao,predict_unidades_administrativas,explain_unidades_administrativas

from classifiers.acesso_a_informacao import requisitos_sitios
from classifiers.acesso_a_informacao import informacoes
from classifiers.acesso_a_informacao import base_dados
# from classifiers.acesso_a_informacao import divulgacao_atendimentos

from classifiers.despesas import empenhos
from classifiers.despesas import pagamentos
from classifiers.despesas import consulta_favorecido
from classifiers.despesas import gerar_relatorio
from classifiers.despesas import relatorios

from classifiers import licitacoes 


keywords = keywords_template

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

    result.to_csv('test.csv', index=False)

    output = add_in_dict(output, 'address', isvalid, result_explain)

    return output

def pipeline_base_dados(keywords, path_base, num_matches, job_name, verbose=False):

    output = {'relação_das_bases': {},
              }

    # Publica na internete relação das bases de dados abertos do município ou do estado
    isvalid, result = base_dados.predict_bases_de_dados_abertos(path_base = path_base, job_name=job_name)
    result_explain = base_dados.explain_bases_de_dados_abertos(isvalid, result)

    print(result_explain)

    output = add_in_dict(output, 'relação_das_bases', isvalid, result_explain)

    return output

def pipeline_divulgacao_atendimentos(keywords, path_base, num_matches, job_name, verbose=False):

    output = {'pedidos_recebidos': {},
              'pedidos_atendidos': {},
              'pedidos_indeferidos': {},
              }

    (isvalid_recebidos, df_recebidos), (isvalid_atendidos,df_atendidos), (isvalid_indeferidos,df_indeferidos) = divulgacao_atendimentos.predict_relatorio_estatistico(path_base = path_base, job_name=job_name)
    
    result_explain_recebidos = divulgacao_atendimentos.explain(df_recebidos, column_name='matches', elemento='pedidos_recebidos', verbose=False)
    result_explain_atendidos = divulgacao_atendimentos.explain(df_atendidos, column_name='matches', elemento='pedidos_atendidos', verbose=False)
    result_explain_indeferidos = divulgacao_atendimentos.explain(df_indeferidos, column_name='matches', elemento='pedidos_indeferidos', verbose=False)
    
    output = add_in_dict(output, 'pedidos_recebidos', isvalid_recebidos, result_explain_recebidos)
    output = add_in_dict(output, 'pedidos_atendidos', isvalid_atendidos, result_explain_atendidos)
    output = add_in_dict(output, 'pedidos_indeferidos', isvalid_indeferidos, result_explain_indeferidos)


    return output

def pipeline_licitacoes(keywords, num_matches, job_name):

    try:
        types = keywords_template['types']
    except KeyError:
        types = 'html'

    search_term = keywords['licitacoes']['search_term']
    keywords_to_search = keywords['licitacoes']['keywords']
    proc_lic_itens = keywords['licitacoes']['proc_lic_itens']
    editais = keywords['licitacoes']['editais']

    output = {
            'proc_lic_numero': {},
            'proc_lic_modalidade': {},
            'proc_lic_objeto': {},
            'proc_lic_status': {},
            'proc_lic_resultado': {},
            'inexigibilidade': {},
            'dispensa': {},
            'editais': {},
            'busca': {}
            }

    #Search
    files = indexing.get_files(
        search_term, num_matches,
        job_name, keywords_search=keywords_to_search)

    files = path_functions.filter_paths(files, words=['licitacao','licitacoes'])
    files = path_functions.agg_paths_by_type2(files)

    validador = licitacoes.Licitacoes(files, proc_lic_itens[0], ttype=types)

    # Procedimentos Licitatórios número
    isvalid, result = validador.predict_df(keyword_check=proc_lic_itens[0])
    result_explain = licitacoes.explain(result, proc_lic_itens[0])
    output = add_in_dict(output, 'proc_lic_numero', isvalid, result_explain)

    # Procedimentos Licitatórios modalidade
    isvalid, result = validador.predict_df(keyword_check=proc_lic_itens[1])
    result_explain = licitacoes.explain(result, proc_lic_itens[1])
    output = add_in_dict(output, 'proc_lic_modalidade', isvalid, result_explain)

    # Procedimentos Licitatórios objeto
    isvalid, result = validador.predict_df(keyword_check=proc_lic_itens[2])
    result_explain = licitacoes.explain(result, proc_lic_itens[2])
    output = add_in_dict(output, 'proc_lic_objeto', isvalid, result_explain)

    # Procedimentos Licitatórios status
    isvalid, result = validador.predict_df(keyword_check=proc_lic_itens[3])
    result_explain = licitacoes.explain(result, proc_lic_itens[3])
    output = add_in_dict(output, 'proc_lic_status', isvalid, result_explain)

    # Procedimentos Licitatórios resultado
    isvalid, result = validador.predict_df(keyword_check=proc_lic_itens[4])
    result_explain = licitacoes.explain(result, proc_lic_itens[4])
    output = add_in_dict(output, 'proc_lic_resultado', isvalid, result_explain)

    # Procedimentos modalidade Inexigibilidade
    isvalid, result = validador.predict_inexibilidade()
    result_explain = licitacoes.explain(result, 'inexigibilidade')
    output = add_in_dict(output, 'inexigibilidade', isvalid, result_explain)

    # Procedimentos modalidade Dispensa
    isvalid, result = validador.predict_dispensa()
    result_explain = licitacoes.explain(result, 'dispensa')
    output = add_in_dict(output, 'dispensa', isvalid, result_explain)

    # Disponibilização de Editais
    isvalid, result = validador.predict_editais(editais)
    result_explain=licitacoes.explain(result, 'editais')
    output = add_in_dict(output, 'editais', isvalid, result_explain)

    # Permite Busca
    isvalid, result = validador.predict_busca()
    result_explain=licitacoes.explain(result, 'busca')
    output = add_in_dict(output, 'busca', isvalid, result_explain)

    return output

def pipeline_empenhos(path_base, job_name, verbose=False):

    output = {'Empenhos - Número': {},
              'Empenhos - Valor': {},
              'Empenhos - Data': {},
              'Empenhos - Favorecido': {},
              'Empenhos - Descrição': {},
              }

    isvalid, result = empenhos.predict_numero(path_base = path_base, job_name=job_name, verbose=verbose)
    result_explain = empenhos.explain(isvalid, result, column_name='isvalid', elemento='Número', verbose=verbose)
    output = add_in_dict(output, 'Empenhos - Número', isvalid, result_explain)

    isvalid, result = empenhos.predict_valor(path_base = path_base, job_name=job_name, verbose=verbose)
    result_explain = empenhos.explain(isvalid, result, column_name='isvalid', elemento='Valor', verbose=verbose)
    output = add_in_dict(output, 'Empenhos - Valor', isvalid, result_explain)

    isvalid, result = empenhos.predict_data(path_base = path_base, job_name=job_name, verbose=verbose)
    result_explain = empenhos.explain(isvalid, result, column_name='isvalid', elemento='Data', verbose=verbose)
    output = add_in_dict(output, 'Empenhos - Data', isvalid, result_explain)

    isvalid, result = empenhos.predict_favorecido(path_base = path_base, job_name=job_name, verbose=verbose)
    result_explain = empenhos.explain(isvalid, result, column_name='isvalid', elemento='Favorecido', verbose=verbose)
    output = add_in_dict(output, 'Empenhos - Favorecido', isvalid, result_explain)

    isvalid, result = empenhos.predict_descricao(path_base = path_base, job_name=job_name, verbose=verbose)
    result_explain = empenhos.explain(isvalid, result, column_name='isvalid', elemento='Descrição', verbose=verbose)
    output = add_in_dict(output, 'Empenhos - Descrição', isvalid, result_explain)

    return output

def pipeline_pagamentos(path_base, job_name, verbose=False):

    output = {'Pagamentos - Valor': {},
              'Pagamentos - Data': {},
              'Pagamentos - Favorecido': {},
              'Pagamentos - Empenho de referência': {},
              }

    isvalid, result = pagamentos.predict_valor(path_base = path_base, job_name=job_name, verbose=verbose)
    result_explain = pagamentos.explain(isvalid, result, column_name='isvalid', elemento='Valor', verbose=verbose)
    output = add_in_dict(output, 'Pagamentos - Valor', isvalid, result_explain)

    isvalid, result = pagamentos.predict_data(path_base = path_base, job_name=job_name, verbose=verbose)
    result_explain = pagamentos.explain(isvalid, result, column_name='isvalid', elemento='Data', verbose=verbose)
    output = add_in_dict(output, 'Pagamentos - Data', isvalid, result_explain)

    isvalid, result = pagamentos.predict_favorecido(path_base = path_base, job_name=job_name, verbose=verbose)
    result_explain = pagamentos.explain(isvalid, result, column_name='isvalid', elemento='Favorecido', verbose=verbose)
    output = add_in_dict(output, 'Pagamentos - Favorecido', isvalid, result_explain)

    isvalid, result = pagamentos.predict_empenho_referencia(path_base = path_base, job_name=job_name, verbose=verbose)
    result_explain = pagamentos.explain(isvalid, result, column_name='isvalid', elemento='Empenho de referência', verbose=verbose)
    output = add_in_dict(output, 'Pagamentos - Empenho de referência', isvalid, result_explain)

    return output

def pipeline_consulta_por_favorecido(path_base, job_name, verbose=False):

    output = {
              'Possibilita consulta de empenhos ou pagamentos por favorecido': {},
              }
    
    isvalid, result = consulta_favorecido.predict_favorecido(path_base = path_base, job_name=job_name, verbose=verbose)
    result_explain = consulta_favorecido.explain(isvalid, result, column_name='matches', elemento='Plano Plurianual', verbose=verbose)
    output = add_in_dict(output, list(output.keys())[0], isvalid, result_explain)

    return output

def pipeline_formato_aberto(path_base, job_name, verbose=False):

    output = {
              'Permite gerar relatório da consulta de empenhos ou de pagamentos em formato aberto': {},
              }

    isvalid, result = gerar_relatorio.predict_relatorio(path_base = path_base, job_name=job_name, verbose=verbose)
    result_explain = gerar_relatorio.explain(isvalid, result, column_name='matches', elemento='Relatório em formato aberto', verbose=verbose)
    output = add_in_dict(output, list(output.keys())[0], isvalid, result_explain)

    return output

def pipeline_relatorios(path_base, job_name, verbose=False):

    output = {
              'Link de acesso ao Plano Plurianual do município': {},
              'Link de acesso à Lei de Diretrizes Orçamentaria do município': {},
              'Link de acesso à Lei Orçamentária Anual do município': {},
              'Apresentação do balanço anual, com as respectivas demonstrações contábeis': {},
              'Relatórios da execução orçamentária e gestão fiscal': {}
              }

    isvalid, result = relatorios.predict_plano_plurianual(path_base = path_base, job_name=job_name, verbose=verbose)
    result_explain = relatorios.explain(isvalid, result, column_name='matches', elemento='Plano Plurianual', verbose=verbose)
    output = add_in_dict(output, 'Link de acesso ao Plano Plurianual do município', isvalid, result_explain)

    isvalid, result = relatorios.predict_lei_diretrizes_orcamentarias(path_base = path_base, job_name=job_name, verbose=verbose)
    result_explain = relatorios.explain(isvalid, result, column_name='matches', elemento='Lei de Diretrizes Orçamentaria', verbose=verbose)
    output = add_in_dict(output, 'Link de acesso à Lei de Diretrizes Orçamentaria do município', isvalid, result_explain)

    isvalid, result = relatorios.predict_lei_orcamentaria_anual(path_base = path_base, job_name=job_name, verbose=verbose)
    result_explain = relatorios.explain(isvalid, result, column_name='matches', elemento='Lei Orçamentária Anual', verbose=verbose)
    output = add_in_dict(output, 'Link de acesso à Lei Orçamentária Anual do município', isvalid, result_explain)

    isvalid, result = relatorios.predict_balanco_demonstracoes(path_base = path_base, job_name=job_name, verbose=verbose)
    result_explain = relatorios.explain(isvalid, result, column_name='matches', elemento='Balanço anual e demonstrações contábeis', verbose=verbose)
    output = add_in_dict(output, 'Apresentação do balanço anual, com as respectivas demonstrações contábeis', isvalid, result_explain)

    isvalid, result = relatorios.predict_execucao_orcamentaria_gestao_fiscal(path_base = path_base, job_name=job_name, verbose=verbose)
    result_explain = relatorios.explain(isvalid, result, column_name='matches', elemento='Relatórios da execução orçamentária e gestão fiscal', verbose=verbose)
    output = add_in_dict(output, 'Relatórios da execução orçamentária e gestão fiscal', isvalid, result_explain)

    return output

def main(jobs,keywords):

    df_all = pd.DataFrame()
    for job_name in jobs:

        print("**",job_name,"**")

        try:
            constant_municipio = 'constant_' + job_name
            tf = open(constant_municipio + ".json", "r")
            keywords = json.load(tf)
        except FileNotFoundError:
            pass

        output_licitacoes = output_licitacoes = pipeline_licitacoes(
                keywords, num_matches, job_name)
        # try:
        #     output_licitacoes = output_licitacoes = pipeline_licitacoes(
        #         keywords, num_matches, job_name)
        # except:
        #     print("erro",job_name )
        #     output_licitacoes = {'proc_lic': {},
        #                         'inexigibilidade': {},
        #                         'resultado': {},
        #                         'dispensa': {},
        #                         'editais': {},
        #                         'busca': {}}

        output_licitacoes['cidade'] = job_name

        # output_informacoes = pipeline_informacoes(
        #     keywords, path_base, num_matches, job_name)
        # output_requisitos_sitios = pipeline_requisitos_sitios(
        #     keywords, path_base, num_matches, job_name)
        output = {
                    # 'cidade':job_name,
                    # 'informacoes': output_informacoes, 
                    # 'requisitos_sitios': output_requisitos_sitios,
                    'licitacoes': output_licitacoes}
        print(output)

        df = pd.DataFrame(output).T
        df_all = pd.concat([df_all, df])
        df_all.to_csv('output_licitacoes.csv', index=False)

    return output

# path_base = '/home/cinthia/F01/data'
path_base = '/home/asafe'
num_matches = 10

jobs = municipios_PT

# jobs = ['engenheiro_navarro']

main(jobs, keywords)