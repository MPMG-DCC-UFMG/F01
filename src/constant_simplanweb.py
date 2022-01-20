# municipios_simplanweb = ["Maripá de Minas",
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
# "Cruzíli",
# "Senhora de Oliveira",
# "Aracitab",
# "Laranjal",
# "Madre de Deus de Minas",
# "São Lourenço",
# "Toledo",
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
# "Volta Grande",
# "Chiador",	
# "Fervedouro",
# "Seritinga",
# "Rio Novo",
# "Andrelândia",
# "Astolfo Dutra",
# "Pedro Teixeira",
# "Tabuleiro",
# "Chácara",
# "Senhora dos Remédio",
# "Guarar",
# "Aiuruoca",
# "Coronel Pacheco",
# "Carmo de Minas",
# "Oratórios",
# "Senador Firmino",
# "Canaã",
# "Ibertioga",
# "Lima Duarte",
# "Teixeira"]

# municipios_formatados = []
# for municipio in municipios_simplanweb:
#     new = (municipio.lower().replace("á","a").replace("â","a").replace("í","i").replace("é","e").replace(" ","_").replace("ã","a").replace("ç","o").replace("ê","e").replace("ó","o"))
#     municipios_formatados.append(new)
# print(municipios_formatados)

# municipios_formatados = ['maripa_de_minas', 'bom_jardim_de_minas', 'bias_fortes', 'ewbank_da_camara', 'simao_pereira', 'cristina', 'guarani', 'piranga', 'passa_vinte', 'barra_longa', 'piau', 'merces', 'rio_espera', 'lamim', 'dom_viooso', 'coimbra', 'bras_pire', 'senador_cortes', 'arantina', 'bocaina_de_minas', 'belmiro_braga', 'cruzili', 'senhora_de_oliveira', 'aracitab', 'laranjal', 'madre_de_deus_de_minas', 'sao_lourenoo', 'toledo', 'amparo_do_serra', 'santana_do_garambeu', 'cipotanea', 'santa_rita_de_ibitipoca', 'rio_preto', 'mirai', 'estrela_dalva', 'olaria', 'diogo_de_vasconcelos', 'paulo_candido', 'minduri', 'rochedo_de_minas', 'volta_grande', 'chiador', 'fervedouro', 'seritinga', 'rio_novo', 'andrelandia', 'astolfo_dutra', 'pedro_teixeira', 'tabuleiro', 'chacara', 'senhora_dos_remedio', 'guarar', 'aiuruoca', 'coronel_pacheco', 'carmo_de_minas', 'oratorios', 'senador_firmino', 'canaa', 'ibertioga', 'lima_duarte', 'teixeira']
# municipioos_to_sheel = ('maripa_de_minas' 'bom_jardim_de_minas' 'bias_fortes' 'ewbank_da_camara' 'simao_pereira' 'cristina' 'guarani' 'piranga' 'passa_vinte' 'barra_longa' 'piau' 'merces' 'rio_espera' 'lamim' 'dom_viooso' 'coimbra' 'bras_pire' 'senador_cortes' 'arantina' 'bocaina_de_minas' 'belmiro_braga' 'cruzili' 'senhora_de_oliveira' 'aracitab' 'laranjal' 'madre_de_deus_de_minas' 'sao_lourenoo' 'toledo' 'amparo_do_serra' 'santana_do_garambeu' 'cipotanea' 'santa_rita_de_ibitipoca' 'rio_preto' 'mirai' 'estrela_dalva' 'olaria' 'diogo_de_vasconcelos' 'paulo_candido' 'minduri' 'rochedo_de_minas' 'volta_grande' 'chiador' 'fervedouro' 'seritinga' 'rio_novo' 'andrelandia' 'astolfo_dutra' 'pedro_teixeira' 'tabuleiro' 'chacara' 'senhora_dos_remedio' 'guarar' 'aiuruoca' 'coronel_pacheco' 'carmo_de_minas' 'oratorios' 'senador_firmino' 'canaa' 'ibertioga' 'lima_duarte' 'teixeira')

keywords_template = {
    'licitacoes': {
       'search_term': 'Licitações licitação',
       'keywords': ["Licitações", "Pregão", "Inexigibilidade", "Homologada", "Resultado Final de Licitação", "Modalidade", "Fundamentação legal", "Status" ],
       'proc_lic_itens': ['número', 'modalidade', 'objeto', 'status', 'editais']
    },
    'types': ['html','bat']
}