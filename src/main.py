import sys
sys.path.insert(1, './classifiers')

#sys.path.insert(0, '/home/cinthia/MPMG/F01/src/classifiers')

# from concursos import predict_copia_edital, explain_copia_edital, predict_recursos, explain_recursos, predict_dados_concurso, explain_dados_concurso
# from diaria_viagem import predict_diaria_viagem, explain_diaria_viagem
# from info_institucionais import predict_estrutura_organizacional,explain_estrutura_organizacional,predict_link_legislacao,explain_link_legislacao,predict_unidades_administrativas,explain_unidades_administrativas

from acesso_a_informacao.informacoes import predict_link_portal, explain_link_portal
from acesso_a_informacao.informacoes import predict_text_expl, explain_text_expl

from acesso_a_informacao.informacoes import predict_legs_federal, explain_legs_federal
from acesso_a_informacao.informacoes import predict_legs_estadual, explain_legs_estadual
from acesso_a_informacao.informacoes import predict_site_transparencia, explain_site_transparencia
from acesso_a_informacao.informacoes import predict_acesso_ilimitado, explain_acesso_ilimitado
from acesso_a_informacao.informacoes import predict_faq, explain_faq

import licitacoes 

if __name__ == "__main__":

    #concursos_dict = predict_dados_concurso()
    #explain_dados_concurso(concursos_dict)

    
    #local onde está o dump
    path_base = "/home/asafe"
    #path_base = "/home/cinthia/MPMG/persistence_area"
    # path_base = "C:/Users/ritar"
    # path_base = "C:/Users/pedro"

    #------------------------------------------INFORMAÇÃO-----------------------------------------

#     Aba denominada “Transparência” no menu principal do sítio eletrônico

    search_term = 'Prefeitura'
    keywords=['Home', 'Menu', 'Transparência', 'Portal', 'Secretarias', 'Legislação']
    isvalid, result = predict_link_portal(
        search_term, keywords, path_base, num_matches=60,
        job_name='index_ipatinga', threshold = 0)
    
    explain_link_portal(isvalid, result)
#     -------


    # Texto padrão explicativo sobre a Lei de Acesso à Informação

    search_term = 'Lei'
    keywords=['LAI', 'Lei de acesso à informação']
    isvalid, result = predict_text_expl(
        search_term, keywords, path_base, num_matches=60,
        job_name='index_pouso_alegre', threshold = 0)
    
    explain_text_expl(isvalid, result)
    # --------


    # Link de acesso à legislação federal sobre a transparência (Lei nº 12.527/2011 e eventual legislação superveniente)

    search_term='Acesso a informao'
    keywords=['http://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12527.htm']
    isvalid, result = predict_legs_federal(
        search_term, keywords, path_base, num_matches=40,
        job_name='index_pouso_alegre', threshold = 0)
    
    explain_legs_federal(isvalid, result)
    # ---------


    # Link de acesso à legislação 'federal' sobre a transparência (Decreto Estadual nº 45.969/2012 e eventual legislação superveniente)

    search_term='Acesso a informao'
    keywords=['https://www.almg.gov.br/consulte/legislacao/completa/completa.html?num=45969&ano=2012&tipo=DEC']
    isvalid, result = predict_legs_estadual(
        search_term, keywords, path_base, num_matches=40,
        job_name='index_pouso_alegre', threshold = 0)
    
    explain_legs_estadual(isvalid, result)
    # ---------

    # Link de acesso ao site da Transparência (www.transparencia.mg.gov.br)

    search_term='Acesso a informao'
    keywords=['www.transparencia.mg.gov.br']
    isvalid, result = predict_site_transparencia(
        search_term, keywords, path_base, num_matches=40,
        job_name='index_pouso_alegre', threshold = 0)
    
    explain_site_transparencia(isvalid, result)
    # ---------

    # Acesso ilimitado a todas as informações públicas disponibilizadas no sítio eletrônico: 
    # o acesso não pode estar condicionado à criação de um cadastro ou ao fornecimento de dados pessoais

    search_term = 'Login'
    keywords=['necessrio efetuar login', 'senha', 'login' 'usuário']
    isvalid, result = predict_acesso_ilimitado(
        search_term, keywords, path_base, num_matches=2600,
        job_name='index_pouso_alegre', threshold = 0)
    
    explain_acesso_ilimitado(isvalid, result)
    # ---------


    # Link de respostas a perguntas mais frequentes da sociedade.
    
    search_term='Perguntas Frequentes'
    keywords=['FAQ', 'Perguntas', 'Respostas']
    isvalid, result = predict_faq(
        search_term, keywords, path_base, num_matches=30,
        job_name='index_pouso_alegre', threshold = 0)

    explain_faq(isvalid, result)
    #--------    




    #------------------------------------------LICITAÇÕES-----------------------------------------

    # search_term="Licitações"
    # keywords_search = ["Licitações", "Pregão", "Inexigibilidade", "Homologada", "Resultado Final de Licitação", "Modalidade", "Fundamentação legal", "Status" ]
    
    # # Procedimentos licitatórios
    # keywords_check=['nmero da licitao', 'modalidade', 'objeto', 'status', 'editais']
    # isvalid, result = licitacoes.predict_proc_lic(
    #     search_term, keywords_search, path_base, num_matches=40,
    #     keywords_check=keywords_check,
    #     filter_word='licitacoes', job_name='index_gv', threshold = 0)

    # for i in range(len(keywords_check)):
    #     print("Predict - Procedimentos Licitatórios - {}: {}".format(keywords_check[i], isvalid[i]))
    #     licitacoes.explain(result['proc_lic'], keywords_check[i])

    # # Procedimentos de Inexigibilidade
    # isvalid, result = licitacoes. predict_inexigibilidade(
    #     search_term, keywords_search, path_base, num_matches=40,
    #     filter_word='licitacoes', job_name='index_gv', threshold=0)

    # print("Predict - Inexigibilidade: {}".format(isvalid))
    # licitacoes.explain(result, 'inexigibilidade')

    # #Resultado
    # isvalid, result = licitacoes.predict_resultado(
    #     search_term='', keywords_search='', path_base=path_base, num_matches=40,
    #     filter_word='licitacoes', job_name='index_gv', threshold=0)

    # licitacoes.explain(result, 'resultado')

    # #Dispensa
    # isvalid, result = licitacoes.predict_dispensa(
    #     search_term='', keywords_search='', path_base=path_base, num_matches=40,
    #     filter_word='licitacoes', job_name='index_gv', threshold=0)

    # licitacoes.explain(result, 'dispensa')

    # # Disponibilização de Editais
    # isvalid, result = licitacoes.predict_editais(
    #     search_term, keywords_search, path_base, num_matches=40,
    #     filter_word='licitacoes', job_name='index_gv', threshold=0)

    # print("Predict - Editais: {}".format(isvalid))
    # licitacoes.explain(result, 'editais')

    # # Permite Busca
    # isvalid, result = licitacoes.predict_busca(
    #     search_term, keywords_search, path_base, num_matches=40,
    #     filter_word='licitacoes', job_name='index_gv', threshold=0)

    # print("Predict - Busca: {}".format(isvalid))
    # print(result)
    # licitacoes.explain(result, 'busca')

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



