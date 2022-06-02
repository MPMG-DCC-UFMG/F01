from utils.path_functions import format_city_names

municipios_template2 = [
# "Novo Oriente de Minas",
# "Frei Gaspar",
# "Fronteira dos Vales",
# "Chapada do Norte",
# "Sardoá",
# "Bertópolis",
# "Cuparaque",
# "Coroaci",
# "Machacalis",
# "Periquito",
# "Itabirinha",
# "São Sebastião do Maranhão",
# "Caraí",
# "Ataléia",
# "Ouro Verde de Minas",
# "Itaipé",
"Umburatiba",
"Marilac",
"Jordânia",
"São João Evangelista",
# "Bandeira",
"Tumiritinga",
"Santa Efigênia de Minas",
"Pavão",
"Pescador",
"Cantagalo",
"Santo Antônio do Jacinto"
]

municipios_template2 = format_city_names(municipios_template2)

keywords_template2 = {
    'licitacoes': {
       'search_term': 'Modalidade Objeto Item Quantidade Licitações',
       'keywords': ["objeto"],
       'proc_lic_itens': ['n° do processo', 'modalidade', 'objeto', 'situação', 'empresa vencedor'],
       'editais': 'Editais de Licitação e Demais Arquivos'
    },
    'types': ['bat','pdf']
}