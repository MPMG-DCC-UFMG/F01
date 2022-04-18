from utils.path_functions import format_city_names

municipios_siplanweb = [
    # "Maripá de Minas",
    # "Bom Jardim de Minas",
    # "Bias Fortes",
    # "Ewbank da Câmara",
    # "Simão Pereira",
    # "Cristina",
    # "Guarani",
    # "Piranga",
    # "Passa Vinte",
    # "Barra Longa",
    # "Piau",
    # "Mercês",
    # "Rio Espera",
    # "Lamim",
    # "Dom Viçoso",
    # "Coimbra",
    # "Brás Pire",
    # "Senador Cortes",
    # "Arantina",
    # "Bocaina de Minas",
    # "Belmiro Braga",
    # "Cruzília",
    # "Senhora de Oliveira",
    # "Aracitaba",
    # "Laranjal",
    # "Madre de Deus de Minas",
    # "São Lourenço",
    "Toledo",
    # "Amparo do Serra",
    # "Santana do Garambéu",
    # "Cipotânea",
    # "Santa Rita de Ibitipoca",
    # "Rio Preto",
    # "Miraí",
    # "Estrela Dalva",
    # "Olaria",
    # "Diogo de Vasconcelos",
    # "Paulo Cândido",
    # "Minduri",
    # "Rochedo de Minas",
##    "Volta Grande",
    # "Chiador",	
    # "Fervedouro",
    # "Seritinga",
    # "Rio Novo",
    # "Andrelândia",
    # "Astolfo Dutra",
    # "Pedro Teixeira",
    # "Tabuleiro",
    # "Chácara",
    # "Senhora dos Remédios",
    # "Guarara",
    # "Aiuruoca",
    # "Coronel Pacheco",
    # "Carmo de Minas",
    # "Oratórios",
    # "Senador Firmino",
    # "Canaã",
    # "Ibertioga",
    # "Lima Duarte",
    # "Teixeira"
]

# print(municipios_formatados)
municipios_siplanweb = format_city_names(municipios_siplanweb)

keywords_siplanweb = {

    'despesas': {
       'search_term': 'Empenho',
       'keywords_to_search': ['Pagamentos','Empenhos', 'despesa', 'empenhado', 'favorecido', 'valor', 'credor'],
       'empenhos': {
                    'numero': 'Empenho', 
                    'valor': 'Vr. Empenhado',
                    'data': 'Data inicial',
                    'favorecido': 'Fornecedor',
                    'descricao': 'Elemento'
                },
    },

    'licitacoes': {
       'search_term': 'Licitações licitação Tomada Modalidade Objeto',
       'keywords': ["Licitações", "Pregão", "Inexigibilidade", "Homologada", "Resultado Final de Licitação", "Modalidade", "Fundamentação legal", "Status", "Objeto" ],
       'proc_lic_itens': ['número', 'modalidade', 'objeto', 'status', 'resultado'],
       'editais': 'Editais de Licitação e Demais Arquivos'
    },
    'types': ['html','bat']

}