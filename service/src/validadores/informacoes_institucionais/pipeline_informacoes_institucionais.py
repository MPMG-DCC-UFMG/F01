from src.validadores.utils import handle_files
from src.validadores.informacoes_institucionais.link_de_acesso import ValidadorLinkDeAcesso

def pipeline_informacoes_institucionais(keywords, job_name):
    try:
        keywords = keywords['informacoes_institucionais']
    except KeyError:
        return None

    # Subtag - Link de Acesso
    validador_link_de_acesso = ValidadorLinkDeAcesso(job_name, keywords['link_de_acesso'])
    output_link_de_acesso = validador_link_de_acesso.predict()

    # result = handle_files.abrir_existente(job_name)
    # print(output_link_de_acesso)
    
    # Link de acesso
    # result['22'] = output_link_de_acesso['link_de_acesso']['predict']

    # handle_files.save_dict_in_json(job_name, result)