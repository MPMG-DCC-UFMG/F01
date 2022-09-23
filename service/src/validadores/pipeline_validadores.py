from src.validadores.acesso_a_informacao.pipeline_acesso_a_informacao import pipeline_acesso_a_informacao 
from src.validadores.receitas.pipeline_receitas import pipeline_receitas 
from src.validadores.licitacoes.pipeline_licitacoes import pipeline_licitacoes
from src.validadores.contratos.pipeline_contratos import pipeline_contratos
from src.validadores.informacoes_institucionais.pipeline_informacoes_institucionais import pipeline_informacoes_institucionais
from src.validadores.terceiro_setor.pipeline_terceiro_setor import pipeline_terceiro_setor
from src.validadores.concursos_publicos.pipeline_concursos_publicos import pipeline_concursos_publicos
from src.validadores.obras_publicas.pipeline_obras_publicas import pipeline_obras_publicas
from src.validadores.servidores.pipeline_servidores import pipeline_servidores
from src.validadores.despesas_com_diarias.pipeline_despesas_com_diarias import pipeline_despesas_com_diarias

def todas_tags(parametros, job_name):

    resultado = {
        'acesso_a_informacao': pipeline_acesso_a_informacao(parametros, job_name),
        'informacoes_institucionais': pipeline_informacoes_institucionais(parametros, job_name),
        'receitas': pipeline_receitas(parametros, job_name),
        'licitacoes': pipeline_licitacoes(parametros, job_name),
        'contratos': pipeline_contratos(parametros, job_name),
        'terceiro_setor': pipeline_terceiro_setor(parametros, job_name),
        'concursos_publicos': pipeline_concursos_publicos(parametros, job_name),
        'obras_publicas': pipeline_obras_publicas(parametros, job_name),
        'despesas_com_diarias': pipeline_despesas_com_diarias(parametros, job_name),
    }

    return resultado

