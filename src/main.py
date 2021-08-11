import sys
sys.path.insert(1, './classifiers')


from concursos import predict_copia_edital, explain_copia_edital, predict_recursos, explain_recursos, predict_dados_concurso, explain_dados_concurso
from diaria_viagem import predict_diaria_viagem, explain_diaria_viagem
from info_institucionais import predict_estrutura_organizacional,explain_estrutura_organizacional,predict_link_legislacao,explain_link_legislacao,predict_unidades_administrativas,explain_unidades_administrativas
from acesso_a_informacao.informacoes import predict_informacoes, explain_informacoes
# from licitacoes import predict_licitacoes, explain_licitacoes

if __name__ == "__main__":

    concursos_dict = predict_dados_concurso()
    explain_dados_concurso(concursos_dict)

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



