
#----------------------------------------- Acesso a informação ----------------------------------------

ABA_TRANSPARENCIA = {
    'index_divinopolis' :  ['http://177.69.246.151/portal/servicos/sonner/transparencia.php'],
    'index_para_de_minas' : ['http://transparencia.parademinas.mg.gov.br/'],
    'index_uberaba' : ['conteudo,37644'], 
    'index_uberlandia' : ['https://www.uberlandia.mg.gov.br/portal-da-transparencia/'], 
    'index_montes_claros' : ['https://transparencia.montesclaros.mg.gov.br/'],
    'index_teofilo_otoni': ['https://transparencia.teofilootoni.mg.gov.br/portalcidadao/#efb33c382dcf9e4ae2294337ce2a566034ee25478c90493e56f55878a4d19d547154abb93a539ca141901243121b0442f68667740d76583a9b6fc842805a701255f50abffb83548323feb3d4a215dcba05fc4b5b868699999c1d78af95bbbed2ae7ab27d940f9f7a8b2debb75557ba1cd7f6303c3be5a0edaecf72a00208c722773c5ec1c75725b2'],
    'index_varginha' : ['http://leideacesso.etransparencia.com.br/varginha.prefeitura.mg/TDAPortalClient.aspx?414'],
    'index_passos' : ['https://sistemas.passos.mg.gov.br/transparencia/'],  
    'index_pouso_alegre': ['https://pousoalegre.atende.net/?pg=transparencia#!/'],
    'index_juiz_de_fora' : '', 
    'index_governador_valadares' :  ['transparencia.valadares.mg.gov.br'],
    'index_ipatinga' : ['http://transparencia.ipatinga.mg.gov.br'],
    'index_betim' : ['http://servicos.betim.mg.gov.br/appsgi/servlet/wmtranspinicial'], 
    'index_congonhas' : ['https://www.congonhas.mg.gov.br/index.php/portal-da-transparencia/'], 
    'index_paracatu' : ['http://200.149.134.10/portalcidadao/#efb33c382dcf9e4ae2294337ce2a566034ee25478c90493e56f55878a4d19d547154abb93a539ca141901243121b0442f68667740d76583a9b6fc842805a701255f50abffb83548323feb3d4a215dcba05fc4b5b868699999c1d78af95bbbed2ae7ab27d940f9f7a8b2debb75557ba1cd7f6303c3be5a0edaecf72a00208c722773c5ec1c75725b2'], 
}


DADOS_ABERTOS = ['API dos dados abertos', 'dados abertos']

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

