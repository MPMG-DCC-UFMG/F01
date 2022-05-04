from utils.path_functions import format_city_names

municipios_siplanweb = [
    "Maripá de Minas",
    "Bom Jardim de Minas",
    "Bias Fortes",
    "Ewbank da Câmara",
    "Simão Pereira",
    "Cristina",
    "Guarani",
    "Piranga",
    "Passa Vinte",
    "Barra Longa",
    "Piau",
    "Mercês",
    "Rio Espera",
    "Lamim",
    "Dom Viçoso",
    "Coimbra",
    "Brás Pires",
    "Senador Cortes",
    "Arantina",
    "Bocaina de Minas",
    "Belmiro Braga",
    "Cruzília",
    "Senhora de Oliveira",
    "Aracitaba",
    "Laranjal",
    "Madre de Deus de Minas",
    "São Lourenço",
    "Toledo",
    "Amparo do Serra",
    "Santana do Garambéu",
    "Cipotânea",
    "Santa Rita de Ibitipoca",
    "Rio Preto",
    "Miraí",
    "Estrela Dalva",
    "Olaria",
    "Diogo de Vasconcelos",
    "Paulo Cândido",
    "Minduri",
    "Rochedo de Minas",
    "Volta Grande",
    "Chiador",	
    "Fervedouro",
    "Seritinga",
    "Rio Novo",
    "Andrelândia",
    "Astolfo Dutra",
    "Pedro Teixeira",
    "Tabuleiro",
    "Chácara",
    "Senhora dos Remédios",
    "Guarara",
    "Aiuruoca",
    "Coronel Pacheco",
    "Carmo de Minas",
    "Oratórios",
    "Senador Firmino",
    "Canaã",
    "Ibertioga",
    "Lima Duarte",
    "Teixeiras"
]

# print(municipios_formatados)
municipios_siplanweb = format_city_names(municipios_siplanweb)

keywords_siplanweb = {

    'despesas': {
       'empenhos': {
            'search_term': 'Empenho',
            'keywords_to_search': ['Pagamentos','Empenhos', 'despesa', 'empenhado', 'favorecido', 'valor', 'credor'],
            'num_matches': 1000,
            'types': ['bat'],
            'numero': 'Empenho', 
            'valor': 'Vr. Empenhado',
            'data': 'Data inicial',
            'favorecido': 'Fornecedor',
            'descricao': 'Elemento'
        },
        'pagamentos': {
            'search_term': 'Pago',
            'keywords_to_search': ['Número','Ano','Emissão','CNPJ','CPF','Tipo','Saldo'],
            'num_matches': 1000,
            'types': ['bat'],
            'valor': 'Val. Pago',
            'data': 'Emissão',
            'favorecido': 'Fornecedor',
            'empenho_de_referencia': 'n'
        },
        'consulta_favorecido':{
            'search_term': 'despesa',
            'keywords_to_search': ['Empenho','Pagamentos','transparencia','filtrar'],
            'num_matches': 1000,
            'types': ['html'],
            'keyword_check': ['Fornecedor']
        },
        'gerar_relatorios':{
            'search_term': 'despesa',
            'keywords_to_search': ['Empenho','Pagamentos','transparencia','filtrar'],
            'num_matches': 500,
            'types': ['html'],
            'keyword_check': ['Gerar PDF','Gerar Excel','Gerar CSV']
        },
        'relatorios':{
            'plano_plurianual':{
                'search_term': 'Plurianual PPA',
                'keywords_to_search': ['PPA', 'Plano Plurianual', 'PPA Lei'],
                'num_matches': 500,
                'types': ['html'],
                'keyword_check': ['Visualizar Documento','Baixar Documento']
            },
            'lei_diretrizes_orcamentarias':{
                'search_term': 'Diretrizes orçamentárias LDO',
                'keywords_to_search': ['Diretrizes orçamentárias', 'metas fiscais', 'lei diretrizes orçamentárias', 'LDO'],
                'num_matches': 500,
                'types': ['html'],
                'keyword_check': ['Visualizar Documento','Baixar Documento']
            },
            'lei_orcamentaria_anual':{
                'search_term': 'anual L.O.A.',
                'keywords_to_search': ['LOA', 'LOA Lei', 'Lei orçamentária anual', 'orçamentária anual'],
                'num_matches': 500,
                'types': ['html'],
                'keyword_check': ['Visualizar Documento','Baixar Documento']
            },
            'balanco_demonstracoes':{
                'search_term': 'Balanço anual Demonstrações Contábeis',
                'keywords_to_search': ['Balanço anual', 'Demonstrações Contábeis', 'Balancete da Despesa', 'Balanço Orçamentário de Despesas', ' Balanço Patrimonial'],
                'num_matches': 500,
                'types': ['html'],
                'keyword_check': ['Visualizar Documento','Baixar Documento']
            },
            'execucao_orcamentaria_gestao_fiscal':{
                'search_term': 'Relatórios execução orçamentária gestão fiscal',
                'keywords_to_search': ['execução orçamentária', 'gestão fiscal', 'execução orçamentaria', 'prestacao_de_contas', 'relatorios de gestao fiscal'],
                'num_matches': 500,
                'types': ['html'],
                'keyword_check': ['Visualizar Documento','Baixar Documento']
            },
        }
    },

    'licitacoes': {
       'search_term': 'Licitações licitação Tomada Modalidade Objeto',
       'keywords': ["Licitações", "Pregão", "Inexigibilidade", "Homologada", "Resultado Final de Licitação", "Modalidade", "Fundamentação legal", "Status", "Objeto" ],
       'proc_lic_itens': ['número', 'modalidade', 'objeto', 'status', 'resultado'],
       'editais': 'Editais de Licitação e Demais Arquivos'
    },
    'types': ['html','bat']

}