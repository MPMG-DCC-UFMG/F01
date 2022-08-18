from utils import handle_files
from validadores.licitacoes.processos_licitatorios import ValidadorProcessosLicitatorios
from validadores.licitacoes.registro_dos_procedimentos import ValidadorRegistroDosProcedimentos
from validadores.licitacoes.editais import ValidadorEditais
from validadores.licitacoes.resultado_das_licitacoes import ValidadorResultadosDasLicitacoes

def pipeline_licitacoes(keywords, job_name):

    # Subtag - Processos Licitatorios
    validador_processos_licitatorios = ValidadorProcessosLicitatorios(job_name, keywords['processos_licitatorios'])
    output_processos_licitatorios = validador_processos_licitatorios.predict()
    print(output_processos_licitatorios)

    # Subtag - Registro dos procedimentos
    validador_registro_dos_procedimentos = ValidadorRegistroDosProcedimentos(job_name, keywords['registro_dos_procedimentos'])
    output_registro_dos_procedimentos = validador_registro_dos_procedimentos.predict()

    # Subtag Editais
    validador_editais = ValidadorEditais(job_name, keywords['editais'])
    output_editais = validador_editais.predict()

    # Resultados das licitações
    validador_resultado_das_licitacoes = ValidadorResultadosDasLicitacoes(job_name, keywords['resultado_das_licitacoes'])
    output_resultado_das_licitacoes = validador_resultado_das_licitacoes.predict()

    print('Licitações:',  output_processos_licitatorios['numero']['predict'], 
                        output_processos_licitatorios['modalidade']['predict'], 
                        output_processos_licitatorios['objeto']['predict'], 
                        output_processos_licitatorios['status']['predict'], 
                        output_processos_licitatorios['resultado']['predict'])    


    result = handle_files.abrir_existente(job_name)
    
    # Processos licitatórios
    result['43'] = output_processos_licitatorios['numero']['predict']
    result['44'] = output_processos_licitatorios['modalidade']['predict']
    result['45'] = output_processos_licitatorios['objeto']['predict']
    result['46'] = output_processos_licitatorios['status']['predict']
    result['47'] = output_processos_licitatorios['resultado']['predict']

    # Registro dos procedimentos
    result['48'] = output_registro_dos_procedimentos['inexigibilidade_e_dispensa']['predict']

    # Editais
    result['49'] = output_editais['editais']['predict']

    # Resultados das licitações 
    result['50'] = output_resultado_das_licitacoes['resultados_das_licitacoes']['predict']


    handle_files.save_dict_in_json(job_name, result)