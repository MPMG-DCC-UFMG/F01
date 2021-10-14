
#----------------------------------------- Acesso a informação ----------------------------------------

ABA_TRANSPARENCIA = {
    'index_divinopolis' :  'http://177.69.246.151/portal/servicos/sonner/transparencia.php',
    'index_para_de_minas' : 'http://transparencia.parademinas.mg.gov.br/',
    'index_uberaba' : 'conteudo,37644', 
    'index_uberlandia' : 'https://www.uberlandia.mg.gov.br/portal-da-transparencia/', 
    'index_montes_claros' : 'https://transparencia.montesclaros.mg.gov.br/',
    'index_teofilo_otoni': 'https://transparencia.teofilootoni.mg.gov.br/portalcidadao/#efb33c382dcf9e4ae2294337ce2a566034ee25478c90493e56f55878a4d19d547154abb93a539ca141901243121b0442f68667740d76583a9b6fc842805a701255f50abffb83548323feb3d4a215dcba05fc4b5b868699999c1d78af95bbbed2ae7ab27d940f9f7a8b2debb75557ba1cd7f6303c3be5a0edaecf72a00208c722773c5ec1c75725b2',
    'index_varginha' : '',
    'index_passsos' : '',  
    'index_pouso_alegre': 'https://pousoalegre.atende.net/?pg=transparencia#!/',
    'index_juiz_de_fora' : '', 
    'index_governador_valadares' :  'transparencia.valadares.mg.gov.br',
    'index_ipatinga' : 'http://transparencia.ipatinga.mg.gov.br',
    'index_betim' : 'http://servicos.betim.mg.gov.br/appsgi/servlet/wmtranspinicial', 
    'index_congonhas' : 'https://www.congonhas.mg.gov.br/index.php/portal-da-transparencia/', 
    'index_paracatu' : 'http://200.149.134.10/portalcidadao/#efb33c382dcf9e4ae2294337ce2a566034ee25478c90493e56f55878a4d19d547154abb93a539ca141901243121b0442f68667740d76583a9b6fc842805a701255f50abffb83548323feb3d4a215dcba05fc4b5b868699999c1d78af95bbbed2ae7ab27d940f9f7a8b2debb75557ba1cd7f6303c3be5a0edaecf72a00208c722773c5ec1c75725b2', 
}

URL_TRANSPARENCIA_MG = ['http://www.transparencia.mg.gov.br/','www.transparencia.mg.gov.br','https://www.transparencia.mg.gov.br/transferencia-de-impostos-a-municipios']

LEI_ACESSO_INFORMACAO = ['Lei Federal 12.527', 'LEI Nº 12.527, DE 18 DE NOVEMBRO DE 2011']

LEI_ACESSO_INFORMACAO_CONTEUDO = [
    'Cabe aos órgãos e entidades do poder público, observadas as normas e procedimentos específicos aplicáveis, assegurar',
    'conhecida como a Lei de Acesso à Informação',
    'Lei Federal 12.527',
    'Sistema Eletrônico de Serviço de Informações ao Cidadão',
    'A Lei de Acesso a Informações no',
    'e-SIC',
    'em cumprimento a Lei nº 12.527',
    'Regula o acesso a informações previsto no inciso' ,
    'aumentando a transparência da gestão pública',
    'Leis que regem o Portal',
    'Regula o acesso a informações previsto',
    'Regulamenta o acesso à informação',
    'Dispõe sobre a disponibilização de informações',
    'Conheça essa legislação',
    'A Lei de Acesso a Informações no Brasil'
    # Possíveis acréscimos:
    # O acesso a informações públicas
    # ficou instituído 
    # viabilizar o acesso
]

LINK_LEGS_FEDERAL = 'http://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12527.htm'
LINK_LEGS_ESTADUAL = 'https://www.almg.gov.br/consulte/legislacao/completa/completa.html?num=45969&ano=2012&tipo=DEC'

ACESSO_ILIMITADO = ['necessrio efetuar login', 'clique aqui para fazer login', 'clique aqui para fazer cadastro', 'para baixar necessrio']

DADOS_ABERTOS = ['API', 'dados abertos']

FAQ = ['Faq', 'FAQ', 'Faq']
FAQ_SEARCH = ['Perguntas Frequentes', 'perguntas frequentes', 'Perguntas', 'perguntas']

GRAVAR = ['pdf', 'xls', 'doc']


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

