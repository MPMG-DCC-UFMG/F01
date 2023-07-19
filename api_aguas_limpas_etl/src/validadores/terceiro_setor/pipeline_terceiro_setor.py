from src.validadores.utils import handle_files
from src.validadores.terceiro_setor import dados_de_parcerias
from src.validadores.terceiro_setor import repasses

def pipeline_terceiro_setor(keywords, job_name):
    try:
        keywords = keywords['terceiro_setor']
    except KeyError:
        return None

    terceiro_setor = {}

    # Subtag - Dados de Parcerias
    try:
        keywords_dados_de_parcerias = keywords['dados_de_parcerias']
        
    except KeyError:
        print(" KeyError - Terceiro Setor - Dados de Parcerias")
    
    validador_dados_de_parceria = dados_de_parcerias.ValidadorDadosDeParcerias(job_name, keywords_dados_de_parcerias)
    terceiro_setor['dados_de_parcerias'] = validador_dados_de_parceria.predict()
    
    return terceiro_setor
    
    # # Subtag - Repasses
    # try:
    #     keywords_repasses = keywords['repasses']
    #     validador_repasses = repasses.ValidadorRepasses(job_name, keywords_repasses)
    #     terceiro_setor['repasses'] = validador_repasses.predict()
    # except KeyError:
    #     return terceiro_setor

    # return terceiro_setor