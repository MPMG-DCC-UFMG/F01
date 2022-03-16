from utils.path_functions import format_city_names

municipios_betha = [
    "Alfenas",
    "Alterosa",
    "Alto Rio Doce",
    "Alvinópolis",
    "Bandeira do Sul",
    "Boa Esperança",
    "Botelhos",
    "Cambuquira",
    "Campos Gerais",
    "Cataguases",
    "Cláudio",
    "Coinceição da Aparecida",
    "Congonhas",
    "Formiga",
    "Guaranésia",
    "Igaratinga",
    "Ijaci",
    "Itapeva",
    "Itatiaiuçu",
    "Lagoa da Prata",
    "Luz",
    "Mantena",
    "Mariana",
    "Nepomuceno",
    "Ouro Branco",
    "Pequi",
    "Pirajuba",
    "Planura",
    "Raposos",
    "Rio Casca",
    "Rio Doce",
    "Sacramento",
    "Santo Antônio do Monte",
    "São Sebastião do Oeste",
    "Sarzedo",
    "Serrania"
]

municipios_betha = format_city_names(municipios_betha)

keywords_template = {
    'licitacoes': {
       'search_term': 'Licitac Dispensa Inexigibi',
       'keywords': ["Licitações", "Pregão", "Inexigibilidade", "Homologada", "Resultado Final de Licitação", "Modalidade", "Status", "Objeto" ],
       'proc_lic_itens': ['nº do processo', 'modalidade', 'objeto', 'situação', 'Editais de Licitação e Demais Arquivos'],
       'editais': 'Editais de Licitação e Demais Arquivos'
    },
    'types': 'html'
}