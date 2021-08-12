import sys
sys.path.insert(1, './classifiers')

#sys.path.insert(0, '/home/cinthia/MPMG/F01/src/classifiers')

# from concursos import predict_copia_edital, explain_copia_edital, predict_recursos, explain_recursos, predict_dados_concurso, explain_dados_concurso
# from diaria_viagem import predict_diaria_viagem, explain_diaria_viagem
# from info_institucionais import predict_estrutura_organizacional,explain_estrutura_organizacional,predict_link_legislacao,explain_link_legislacao,predict_unidades_administrativas,explain_unidades_administrativas
# from acesso_a_informacao.informacoes import predict_informacoes, explain_informacoes
import licitacoes 

if __name__ == "__main__":

    #concursos_dict = predict_dados_concurso()
    #explain_dados_concurso(concursos_dict)


    
    #local onde está o dump
    path_base = "/home/cinthia/MPMG/persistence_area"
    # path_base = "C:/Users/ritar"
    # path_base = "C:/Users/pedro"

    search_term="Licitações"
    keywords_search = ["Licitações", "Pregão", "Inexigibilidade", "Homologada", "Resultado Final de Licitação", "Modalidade", "Fundamentação legal", "Status" ]
    
    # Procedimentos licitatórios
    keywords_check=['nmero da licitao', 'modalidade', 'objeto', 'status', 'editais']
    isvalid, result = licitacoes.predict_proc_lic(
        search_term, keywords_search, path_base, num_matches=40,
        keywords_check=keywords_check,
        filter_word='licitacoes', job_name='index_gv', threshold = 0)

    for i in range(len(keywords_check)):
        print("Predict - Procedimentos Licitatórios - {}: {}".format(keywords_check[i], isvalid[i]))
        licitacoes.explain(result['proc_lic'], keywords_check[i])

    # Procedimentos de Inexigibilidade
    isvalid, result = licitacoes. predict_inexigibilidade(
        search_term, keywords_search, path_base, num_matches=40,
        filter_word='licitacoes', job_name='index_gv', threshold=0)

    print("Predict - Inexigibilidade: {}".format(isvalid))
    licitacoes.explain(result, 'inexigibilidade')

    # Disponibilização de Editais
    isvalid, result = licitacoes.predict_editais(
        search_term, keywords_search, path_base, num_matches=40,
        filter_word='licitacoes', job_name='index_gv', threshold=0)

    print("Predict - Editais: {}".format(isvalid))
    licitacoes.explain(result, 'editais')

    # Permite Busca
    isvalid, result = licitacoes.predict_busca(
        search_term, keywords_search, path_base, num_matches=40,
        filter_word='licitacoes', job_name='index_gv', threshold=0)

    print("Predict - Busca: {}".format(isvalid))
    licitacoes.explain(result, 'busca')

    # concursos_dict = predict_copia_edital()
    # explain_copia_edital(concursos_dict)
    
    # concursos_dict = predict_recursos()
    # explain_recursos(concursos_dict)


    # licitacoes_dict = predict_licitacoes()
    # explain_licitacoes(licitacoes_dict)
    
    # estrutura_bool = predict_estrutura_organizacional()
    # explain_estrutura_organizacional()

    # link_legislacao_bool = predict_link_legislacao()
    # explain_link_legislacao()

    # unidades_dict = predict_unidades_administrativas()
    # explain_unidades_administrativas()

    # ----------------------- Acesso a informação --------------------------
    # informacoes_dict = predict_informacoes()
    # explain_informacoes(informacoes_dict)



