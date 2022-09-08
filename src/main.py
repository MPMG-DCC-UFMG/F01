# from utils.indexing import remove_index
from pipeline_acesso_a_informacao import pipeline_acesso_a_informacao
from pipeline_receitas import pipeline_receitas 
# from pipeline_despesas import pipeline_despesas
from pipeline_licitacoes import pipeline_licitacoes
from pipeline_contratos import pipeline_contratos
from pipeline_informacoes_institucionais import pipeline_informacoes_institucionais
from pipeline_terceiro_setor import pipeline_terceiro_setor
from pipeline_concursos_publicos import pipeline_concursos_publicos
from pipeline_obras_publicas import pipeline_obras_publicas
from pipeline_servidores import pipeline_servidores
from pipeline_despesas_com_diarias import pipeline_despesas_com_diarias

from utils.handle_files import get_municipios_do_template
from utils.handle_files import get_keywords_do_template

def main(template): 
    print("Rodando validadores:")

    parametros = get_keywords_do_template(template)
    municipios = get_municipios_do_template(template)

    for municipio in municipios:
            # if municipio == "formiga":
            # if municipio == "ponto_chique":
            # if municipio == "guanhaes":
            if municipio == "muriae":
                print(municipio)
                pipeline_acesso_a_informacao(parametros['acesso_a_informacao'], municipio)
                # pipeline_informacoes_institucionais(parametros['informacoes_institucionais'], municipio)
                # pipeline_receitas(parametros['receitas'], municipio)
                # pipeline_licitacoes(parametros['licitacoes'], municipio)
                # pipeline_contratos(parametros['contratos'], municipio)
                # pipeline_terceiro_setor(parametros['terceiro_setor'], municipio)
                # pipeline_concursos_publicos(parametros['concursos_publicos'], municipio)
                # pipeline_obras_publicas(parametros['obras_publicas'], municipio)
                # pipeline_despesas_com_diarias(parametros['despesas_com_diarias'], municipio)

            # Em dev
                # pipeline_servidores(parametros['servidores'], municipio)

if __name__ == '__main__':

    # template = 'sintese'
    # template = 'betha'
    # template = 'siplanweb'
    template = 'abo'
    main(template)


path_base = '/home/asafe'

def pipeline_requisitos_sitios(keywords, path_base, num_matches, job_name, verbose=False):

    output = {'search_engine': {},
              'export_reports': {},
              'update_infos': {},
              'accessibility': {},
              'address': {}}

    #Contém ferramenta de pesquisa
    search_term = keywords['search_engine']['search_term']
    keywords_to_search = keywords['search_engine']['keywords']

    isvalid, result = requisitos_exigidos.predict_search_engine(
        search_term=search_term, keywords=keywords_to_search,
        job_name=job_name, path_base=path_base,
            verbose=verbose)
    result_explain = requisitos_exigidos.explain(
        result, column_name='matches', elemento='Possui ferramenta de pesquisa', verbose=verbose)

    output = add_in_dict(output, 'search_engine', isvalid, result_explain)

    # Possibilita gravação de relatórios
    search_term = keywords['export_reports']['search_term']
    keywords_to_search = keywords['export_reports']['keywords']

    isvalid, result = requisitos_exigidos.predict_export_reports(
        search_term=search_term, keywords=keywords_to_search,
        job_name=job_name, path_base=path_base, 
            verbose=verbose)
    result_explain  = requisitos_exigidos.explain(
        result, column_name='matches', elemento='Permite exportar relatórios', verbose=verbose)

    output = add_in_dict(output, 'export_reports', isvalid, result_explain)

    # Mantém as informações atualizadas
    search_term = keywords['update_infos']['search_term']
    keywords_to_search = keywords['update_infos']['keywords']

    isvalid, result = requisitos_exigidos.predict_update_infos(
        search_term=search_term, keywords=keywords_to_search,
        job_name=job_name, path_base=path_base, 
        verbose=verbose)
    result_explain = requisitos_exigidos.explain(
        result, column_name='matches', elemento='Mantém as informações atualizadas', verbose=verbose)

    output = add_in_dict(output, 'update_infos', isvalid, result_explain)

    # Possui mecanismos de acessibilidade
    search_term = keywords['accessibility']['search_term']
    keywords_to_search = keywords['accessibility']['keywords']

    isvalid, result = requisitos_exigidos.predict_accessibility (
        search_term=search_term, keywords=keywords_to_search,
        job_name=job_name, path_base=path_base, 
        verbose=verbose)
    result_explain = requisitos_exigidos.explain(
        result, column_name='matches', elemento='Possui mecanismos de acessibilidade', verbose=verbose)

    output = add_in_dict(output, 'accessibility', isvalid, result_explain)

    # Possui local e instruções para fácil acesso do interessado à comunicação com o município
    search_term = keywords['address']['search_term']
    keywords_to_search = keywords['address']['keywords']

    isvalid, result = requisitos_exigidos.predict_address(
        search_term=search_term, keywords=keywords_to_search,
        job_name=job_name, path_base=path_base, 
            verbose=verbose)
    result_explain = requisitos_exigidos.explain(
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

