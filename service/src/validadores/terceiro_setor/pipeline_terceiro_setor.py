from src.validadores.utils import handle_files
from src.validadores.terceiro_setor import dados_de_parcerias
from src.validadores.terceiro_setor import repasses

def pipeline_terceiro_setor(keywords, job_name):
    try:
        keywords = keywords['terceiro_setor']
    except KeyError:
        return None

    terceiro_setor = {
        'dados_de_parcerias': {},
        'repasses': {}
    }

    # Subtag - Dados de Parcerias
    # validador_dados_de_parceria = dados_de_parcerias.ValidadorDadosDeParcerias(job_name, keywords['dados_de_parcerias'])
    # output_dados_de_parceria = validador_dados_de_parceria.predict()
    # print(output_dados_de_parceria)


    # Subtag - Repasses
    validador_repasses = repasses.ValidadorRepasses(job_name, keywords['repasses'])
    terceiro_setor['repasses'] = validador_repasses.predict()

    return terceiro_setor