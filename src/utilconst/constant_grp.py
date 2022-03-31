from utils.path_functions import format_city_names

municipios_grp = [
    # "Carneirinho",
    # "Conquista",
    # "Caxambu",
    # "São José da Lapa",
    # "Capinópolis",
    # "Guaxupé",
    # "Dores do Indaiá",
    "Andradas",
    # "Canápolis",
    # "Santa Vitória",
    # "Frutal",
    # "Lagoa Santa",
    # "Igarapé",
    # "Coronel Fabriciano",
    # "Gurinhatã",
    # "Paracatu",
    # "Teófilo Otoni",
    # "São Joaquim de Bicas",
    "Prata",
    # "Poços de Caldas",
    # "Cachoeira Dourada",
    # "Itanhandu",
    # "Araguari",
    # "União de Minas",
    # "Lavras",
    # "Unaí",
    # "Divinópolis"
]

municipios_grp = format_city_names(municipios_grp)

keywords_grp = {
    'licitacoes': {
       'search_term': 'Licitatórios',
       'keywords': ['objeto', 'modalidade', 'situação'],
       'proc_lic_itens': ['processo', 'modalidade', 'objeto', 'situação', 'empresa vencedor'],
       'editais': 'Editais de Licitação e Demais Arquivos'
    },
    'types': ['bat']
}