from utils.path_functions import format_city_names

municipios_PT = [
#     "Barroso",
#     "Casa Grande",
#     "Luminárias",
#     "Catas Altas da Noruega",
#     "Dores de Campos",
    "Careaçu",
    "São Brás do Suaçuí",
#     "Nazareno",
#     "Entre Rios de Minas",
    "Santana dos Montes",
#     "Conceição da Barra de Minas",
#     "Coronel Xavier Chaves",
    "Carandaí",
#     "Santa Bárbara do Tugúrio",
#     "São Vicente de Minas",
#     "Ressaquinha",
#     "Itumirim",
#     "Tiradentes",
    "Visconde do Rio Branco",
#     "Itutinga",
#     "Carrancas",
#     "Rio Acima",
#     "Jeceaba",
#     "Descoberto",
#     "Queluzito",
    "Ibituruna",
#     "Santa Cruz de Minas",
    "São João del Rei",
#     "Prados",
#     "Antônio Carlos",
    "Alfredo Vasconcelos",
#     "Ingaí",
#     "São Tiago",
#     "Belo Vale",
#     "Santana do Jacaré",
#     "São Geraldo",
    "Silveirânia",
    "Ritápolis",
    "Resende Costa",
    "Ervália",
#     "Conceição dos Ouros",
#     "Lagoa Dourada",
    "Piedade do Rio Grande"
]

# municipios_PT = ["Ibituruna"]

municipios_PT = format_city_names(municipios_PT)

keywords_template = {
    'licitacoes': {
       'search_term': 'Licitac Modalidade Inexigibi',
       'keywords': ["Licitações", "Pregão", "Inexigibilidade", "Homologada", "Resultado Final de Licitação", "Modalidade", "Fundamentação legal", "Status", "Objeto" ],
       'proc_lic_itens': ['n° processo', 'modalidade', 'objeto', 'situação', 'Editais de Licitação e Demais Arquivos'],
       'editais': 'Editais de Licitação e Demais Arquivos'
    },
    'types': 'bat'
}