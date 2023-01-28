from src.validadores.utils import handle_files
from src.validadores.obras_publicas.dados_para_acompanhamento import ValidadorDadosParaAcompanhamento

def pipeline_obras_publicas(keywords, job_name):
    try:
        keywords = keywords['obras_publicas']
    except KeyError:
        return None

    obras_publicas = {
        'dados_para_acompanhamento': {},
    }

    # Subtag - Dados para acompanhamento
    validador_dados_para_acompanhamento = ValidadorDadosParaAcompanhamento(job_name, keywords['dados_para_acompanhamento'])
    obras_publicas['dados_para_acompanhamento'] = validador_dados_para_acompanhamento.predict()

    result = handle_files.abrir_existente(job_name)
    
    # Dados para acompanhamento
    result['71'] = obras_publicas['dados_para_acompanhamento']['objeto']['predict']
    result['72'] = obras_publicas['dados_para_acompanhamento']['valor_total']['predict']
    result['73'] = obras_publicas['dados_para_acompanhamento']['empresa_contratada']['predict']
    result['74'] = obras_publicas['dados_para_acompanhamento']['data_de_inicio']['predict']
    result['75'] = obras_publicas['dados_para_acompanhamento']['data_prevista_ou_prazo_de_execucao']['predict']
    result['76'] = obras_publicas['dados_para_acompanhamento']['valor_total_pago_ou_percentual']['predict']
    result['77'] = obras_publicas['dados_para_acompanhamento']['situacao_atual']['predict']

    handle_files.save_dict_in_json(job_name, result)

    return obras_publicas