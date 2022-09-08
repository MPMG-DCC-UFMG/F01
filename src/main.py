

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

