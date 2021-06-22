URL = 'https://transparencia.valadares.mg.gov.br/'
CONTRATOS = ['Contratos e Aditivos', 'Contratos', 'CONTRATOS', 'contratos']
LICITACOES = ['Licitações', 'Licitacoes']

ORDEM_LICITACOES = {
    'registro': ['status', 'andamento', 'concluida'],
    'situacao' : ['Anulada','Cancelada','Deserta','Em andamento','Encerrada','Fracassada','Homologada', 'Revogada', 'Suspensa' ],
    'ordem' : ['ordenar por', 'data crescente', 'data decrescente', 'número crescente', 'número descente', 'data de abertura', 'data de publicação', 'data de publicações'],
    'tipo' : ['Adesão Registro de Preço','Carta Convite','Chamada Pública','Concorrência','Concurso','Dispensa','Inexigibilidade','Leilão','Pregão','Pregão Eletrônico','Pregão Presencial','Regime Diferenciado de Contratações Públicas','Tomada de Preços']
}


OBJETO_LICITACOES = ['obejto', 'detalhamento do objeto']

SITUACAO_LICITACOES = ['anulada', 'cancelada', 'deserta', 'andamento', 'encerrada', 'fracassada', 'homologada', 'revogada', 'suspensa' ]


#Legislação
CHECKLIST_CONTRATOS = {
    'registro': [],
    'desc_objeto' : ['Objeto'],
    'licitacao_origem' : ['Licitação'],
}
