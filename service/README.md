# F01
Um sistema em Flask para gerenciamento dos resultados da trilha F01 em um banco de dados

Criar banco:

1) set FLASK_APP=app.py

2) flask db init

3) flask db migrate

4) flask db upgrade

<!-- URL utilizadas -->


/municipio/carregar_municipios -> 
    Cadastra os muncipios no banco pela planilha de "lista_municipios.csv" e coloca a url do portal e da prefeitura conforma a planilha "links_validados.csv"

/empresa/cadastrar_templates -> 
    Associa os templates aos municipios, conforme o csv "municipios_clusters.csv"



