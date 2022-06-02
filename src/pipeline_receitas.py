from utils import salvar_resultado
from validadores.receitas import dados_das_receitas

def pipeline_receitas(keywords, job_name):

    # Subtag - dados_das_receitas
    validador_dados_das_receitas = dados_das_receitas.ValidadorDadosDasReceitas(job_name, keywords['dados_das_receitas'])
    output_dados_das_receitas = validador_dados_das_receitas.predict()

    result = salvar_resultado.abrir_existente(job_name)
    print(output_dados_das_receitas['previsao']['predict'], output_dados_das_receitas['arrecadacao']['predict'], output_dados_das_receitas['classificacao']['predict'])    

    result['24'] = output_dados_das_receitas['previsao']['predict']
    result['25'] = output_dados_das_receitas['arrecadacao']['predict']
    result['26'] = output_dados_das_receitas['classificacao']['predict']

    salvar_resultado.save_dict_in_json(job_name, result)