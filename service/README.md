# F01
Um sistema em Flask para gerenciamento dos resultados da trilha F01 em um banco de dados

<!-- Criar banco:

1) set FLASK_APP=app.py

2) flask db init

3) flask db migrate

4) flask db upgrade -->


## URLs utilizadas para configuração:


* Cadastra os muncipios no banco pela planilha de "lista_municipios.csv" e coloca a url do portal e da prefeitura conforma a planilha "links_validados.csv"
```
/municipio/carregar_municipios -> 
```
    
* Associa os templates aos municipios, conforme o csv "municipios_clusters.csv"
```
/empresa/cadastrar_templates -> 
```

* Cadastra a checklist no banco pela planilha "lista_exigencias.csv"
```
/checklist/cadastrar_checklist
```

* Pegar todas as issues de erro de coleta do github e coloca no banco.

```
/carregar_resultados_github ->
```

* Indexar arquivos no ElasticSearch.

```
/indexar_arquivos/<string:nome_do_template>
```


* Gerar csv com os resultados

```
/api/gerar_csv
```