
#----------------------------------------- Acesso a informação ----------------------------------------
ABA_TRANSPARENCIA = 'http://transparencia.valadares.mg.gov.br/'
URL_TRANSPARENCIA_MG = 'www.transparencia.mg.gov.br'

LEI_ACESSO_INFORMACAO = ['Lei Federal 12.527', 'LEI Nº 12.527, DE 18 DE NOVEMBRO DE 2011']

LEI_ACESSO_INFORMACAO_CONTEUDO = [
    'Cabe aos órgãos e entidades do poder público, observadas as normas e procedimentos específicos aplicáveis, assegurar',
    'Lei Federal 12.527',
    'Sistema Eletrônico de Serviço de Informações ao Cidadão',
    'e-SIC',
]

LINK_LEGS_FEDERAL = ['http://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12527.htm']

DADOS_ABERTOS = ['API', 'dados abertos']

FAQ = ['Faq', 'FAQ', 'Faq']
FAQ_SEARCH = ['Perguntas Frequentes', 'perguntas frequentes', 'Perguntas', 'perguntas']

# ---------------------------------------- Concursos --------------------------------------------------
CONCURSO_PUBLICO = 'Concurso Público'
CONCURSO_PUBLICO_KEYWORDS = ['Edital', 'Recursos', 'Aprovados', 'Nomeação', 'edital', 'convocados', 'remanescentes', 'recursos aprovados', 
                            'avaliação psicológica', 'carater eliminatório']
CHECKLIST_CONCURSO_SEARCH = {
    'copia_digital': ['Edital'],
    'recursos': ['Recursos', 'Aprovados'],
    'resultado':['Aprovados'],
    'nomeacao': 'Nomeação',
    'status':['Status', 'Andamento', 'COMUNICADO', 'Comunicado']
}

# ----------------------------------- Diarias de Viagem --------------------------------------

DIARIA_VIAGEM = ['Despesas por Diárias']
DIARIA_VIAGEM_KEYS = []
#Reserva de Viagem
CHECKLIST_VIAGEM_SEARCH = {
    'nome':['nome', 'favorecido', 'beneficiario'],
    'cargo': ['cargo', 'atribuição'],
    'valor_total':['valor'],
    'periodo': ['periodo', 'ano'],
    'destino': ['destino'],
    'atividade':['descricao', 'motivo', 'atividade empenhada'],
    'num_diarias':['numero de diarias'],
}
  
URL = 'https://transparencia.valadares.mg.gov.brs'
LEGISLACAO_MUNICIPAL = ['Legislação Municipal', 'Regulamentação Municipal']
ORGANIZACAO = ['Estrutura Organizacional', 'estrutura organizacional', 'ESTRUTURA ORGANIZACIONAL', 'Organograma', 'Estrutura Administrativa']


# ------------------------------------------ Licitações -----------------------------------------------------------


ORDEM_LICITACOES = {
    'ordem' : ['ordenar por', 'data crescente', 'data decrescente', 'número crescente', 'número descente', 'data de abertura', 'data de publicação', 'data de publicações'],
    'tipo' : ['Dispensa','Inexigibilidade']
}

OBJETO_LICITACOES = ['objeto', 'detalhamento do objeto']

SITUACAO_LICITACOES = ['anulada', 'cancelada', 'deserta', 'andamento', 'encerrada', 'fracassada', 'homologada', 'revogada', 'suspensa' ]

