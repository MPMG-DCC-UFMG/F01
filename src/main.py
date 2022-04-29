import json
import pipeline_despesas
from validadores import licitacoes
from utils.indexing import remove_index

from utils import indexing
from utils import path_functions

# Siplanweb
from utilconst.constant_siplanweb import municipios_siplanweb
from utilconst.constant_siplanweb import keywords_siplanweb
# PT
from utilconst.constant_pt import municipios_PT
from utilconst.constant_pt import keywords_PT
# Betha
from utilconst.constant_betha import municipios_betha
from utilconst.constant_betha import keywords_betha
# Template2
from utilconst.constant_template2 import municipios_template2
from utilconst.constant_template2 import keywords_template2
# GRP
from utilconst.constant_grp import municipios_grp
from utilconst.constant_grp import keywords_grp

# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument("job")
# args = parser.parse_args()

# from concursos import predict_copia_edital, explain_copia_edital, predict_recursos, explain_recursos, predict_dados_concurso, explain_dados_concurso
# from diaria_viagem import predict_diaria_viagem, explain_diaria_viagem
# from info_institucionais import predict_estrutura_organizacional,explain_estrutura_organizacional,predict_link_legislacao,explain_link_legislacao,predict_unidades_administrativas,explain_unidades_administrativas

from validadores.acesso_a_informacao import requisitos_sitios
from validadores.acesso_a_informacao import informacoes
from validadores.acesso_a_informacao import base_dados
# from validadores.acesso_a_informacao import divulgacao_atendimentos

from validadores.despesas import relatorios


path_base = '/home/asafe'
num_matches = 1000

def save_json(job_name, result):
    with open('results/' + job_name + '.json', 'w') as json_file:
        json.dump(result, json_file, 
                            indent=4,  
                            separators=(',',': '))

def add_in_dict(output, item, isvalid, result_explain):
    """
        Responsável por adicionar dicionário o resuiltado da validação
        
        Parameters
        ----------

        output : dicionário com cada chave sendo um item a ser validado
        item : nome da chave referente ao item
        isvalid : resultado do predict
        result_explain: resultado do explain
            
        Returns
        -------
        output
            o dicionário com o predict e o explain adicionado.        
    """
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
        types = keywords['types']
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
            'inexigibilidade_e_dispensa': {},
            'editais': {},
            'busca': {}
            }

    #Search
    files = indexing.get_files(
        search_term, num_matches,
        job_name, keywords_search=keywords_to_search)
    
    files = path_functions.filter_paths(files, words=['licitacao','licitacoes'])
    files = path_functions.agg_paths_by_type(files)
    # print('bat', len(files['bat']))
    # print('pdf', len(files['pdf']))
    validador = licitacoes.ValidadorLicitacoes(files, proc_lic_itens[0], ttype=types)
    # print(len(validador.files['bat']))

    # Procedimentos Licitatórios número
    isvalid, result = validador.predict_df(keyword_check=proc_lic_itens[0])
    result_explain = validador.explain(result, proc_lic_itens[0])
    output = add_in_dict(output, 'proc_lic_numero', isvalid, result_explain)
    
    # Procedimentos Licitatórios modalidade
    isvalid, result = validador.predict_df(keyword_check=proc_lic_itens[1])
    result_explain = validador.explain(result, proc_lic_itens[1])
    output = add_in_dict(output, 'proc_lic_modalidade', isvalid, result_explain)

    # Procedimentos Licitatórios objeto
    isvalid, result = validador.predict_df(keyword_check=proc_lic_itens[2])
    result_explain = validador.explain(result, proc_lic_itens[2])
    output = add_in_dict(output, 'proc_lic_objeto', isvalid, result_explain)

    # Procedimentos Licitatórios status
    isvalid, result = validador.predict_df(keyword_check=proc_lic_itens[3])
    result_explain = validador.explain(result, proc_lic_itens[3])
    output = add_in_dict(output, 'proc_lic_status', isvalid, result_explain)

    # Procedimentos Licitatórios resultado
    isvalid, result = validador.predict_df(keyword_check=proc_lic_itens[4])
    result_explain = validador.explain(result, proc_lic_itens[4])
    output = add_in_dict(output, 'proc_lic_resultado', isvalid, result_explain)

    # # Procedimentos modalidade Inexigibilidade e Dispensa
    isvalid_inexigibilidade, result_inexigibilidade = validador.predict_inexibilidade()
    isvalid_dispensa, result_dispensa = validador.predict_dispensa()
    isvalid = isvalid_inexigibilidade and isvalid_dispensa 
    result = result_inexigibilidade['inexigibilidade']
    result.extend(result_dispensa['dispensa'])
    result = {'inexigibilidade e dispensa': result} 
    result_explain = validador.explain(result, 'inexigibilidade e dispensa')
    output = add_in_dict(output, 'inexigibilidade_e_dispensa', isvalid, result_explain)

    # # Disponibilização de Editais
    isvalid, result = validador.predict_editais(editais)
    result_explain=validador.explain(result, 'editais')
    output = add_in_dict(output, 'editais', isvalid, result_explain)

    # # Permite Busca
    isvalid, result = validador.predict_busca()
    result_explain=validador.explain(result, 'busca')
    output = add_in_dict(output, 'busca', isvalid, result_explain)

    return output


def main(jobs, keywords):

    for job_name in jobs:

        print("**",job_name,"**")
        pipeline_despesas(keywords['despesas'], job_name)

        # print(output_empenhos)



        # output_licitacoes = pipeline_licitacoes(keywords, num_matches, job_name)
        # output_licitacoes['cidade'] = job_name
        # print(output_licitacoes)

        # try:
        #     output_licitacoes = pipeline_licitacoes(keywords, num_matches, job_name)
        #     output_licitacoes['cidade'] = job_name

        #     output = {
        #                 '43': output_licitacoes['proc_lic_numero']['predict'],
        #                 '44': output_licitacoes['proc_lic_modalidade']['predict'],
        #                 '45': output_licitacoes['proc_lic_objeto']['predict'],
        #                 '46': output_licitacoes['proc_lic_status']['predict'],
        #                 '47': output_licitacoes['proc_lic_resultado']['predict'],
        #                 '48': output_licitacoes['inexigibilidade_e_dispensa']['predict'],
        #                 '49': output_licitacoes['editais']['predict'],
        #                 '50': output_licitacoes['busca']['predict'],
        #             }
        #     print(output)
        #     # with open('results/' + job_name + '.json' , 'w') as fp:
        #     #     json.dump(output, fp)

        # except:
        #     print("erro",job_name )
            
        # df = pd.DataFrame(output).T
        # df_all = pd.concat([df_all, df])
        # df_all.to_csv('output_licitacoes.csv', index=False)


# main(municipios_PT, keywords_PT)
# main(municipios_template2, keywords_template2)
# main(municipios_grp, keywords_grp)
main(municipios_siplanweb, keywords_siplanweb)


