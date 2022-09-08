from src.validadores.utils import handle_files
from src.validadores.concursos_publicos.dados_do_concurso import ValidadorDadosDoConcurso
from src.validadores.concursos_publicos.copia_do_edital import ValidadorCopiaDoEdital
from src.validadores.concursos_publicos.divulgacao import ValidadorDivulgacaoRecursosDecisoes	

def pipeline_concursos_publicos(keywords, job_name):

    # Subtag - Dados dos Concursos
    validador_dados_do_concurso = ValidadorDadosDoConcurso(job_name, keywords['dados_do_concurso'])
    output_dados_do_concurso = validador_dados_do_concurso.predict()
    print(output_dados_do_concurso)

    # Subtag - Cópia do edital do concurso	
    validador_copia_do_edital = ValidadorCopiaDoEdital(job_name, keywords['copia_do_edital'])
    output_copia_do_edital = validador_copia_do_edital.predict()
    print(output_copia_do_edital)

    # # Subtag - Divulgação dos recursos e respectivas decisões		
    validador_divulgacao = ValidadorDivulgacaoRecursosDecisoes(job_name, keywords['divulgacao_dos_recursos_e_respectivas_decisoes'])
    output_divulgacao = validador_divulgacao.predict()
    print(output_divulgacao)

    result = handle_files.abrir_existente(job_name)
    
    # Dados dos Concursos
    result['66'] = output_dados_do_concurso['status']['predict']
    result['67'] = output_dados_do_concurso['resultado']['predict']
    result['68'] = output_dados_do_concurso['atos_de_nomeacao']['predict']

    # Cópia do edital do concurso	
    result['69'] = output_copia_do_edital['copia_do_edital']['predict']

    # Divulgação dos recursos e respectivas decisões	
    result['70'] = output_divulgacao['divulgacao_dos_recursos_e_respectivas_decisoes']['predict']

    handle_files.save_dict_in_json(job_name, result)