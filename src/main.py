import sys
sys.path.insert(1, './classifiers')


from faq import predict_faq, explain_faq
from concursos import predict_copia_edital, explain_copia_edital, predict_recursos, explain_recursos
from diaria_viagem import predict_diaria_viagem, explain_diaria_viagem
from info_institucionais import predict_estrutura_organizacional,explain_estrutura_organizacional,predict_link_legislacao,explain_link_legislacao,predict_unidades_administrativas,explain_unidades_administrativas
from acesso_a_informacao import predict_informacoes, explain_informacoes

if __name__ == "__main__":

    faq_dict = predict_faq()
    explain_faq(faq_dict)

    concursos_dict = predict_copia_edital()
    explain_copia_edital(concursos_dict)
    
    concursos_dict = predict_recursos()
    explain_recursos(concursos_dict)


    df = predict_diaria_viagem()
    explain_diaria_viagem(df)
    
    estrutura_bool = predict_estrutura_organizacional()
    explain_estrutura_organizacional()

    link_legislacao_bool = predict_link_legislacao()
    explain_link_legislacao()

    unidades_dict = predict_unidades_administrativas()
    explain_unidades_administrativas()

    # ----------------------- Acesso a informação --------------------------
    informacoes_dict = predict_informacoes()
    explain_informacoes(informacoes_dict)



