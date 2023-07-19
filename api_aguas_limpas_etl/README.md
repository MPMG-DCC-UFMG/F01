## Documentação | Painel Águas Limpas API

Uma API para execução de validadores e gerenciamento dos resultados para fornecer relatório de cumprimento da lei de Acesso à Informação pelos Portais Transparência dos 853 municípios do Estado de Minas Gerais.

> #### Clonando o projeto
> No terminal, acesse o diretório e execute o comando:
> ~~~
> git clone http://gitlab-gsi-prod01.gsi.mpmg.mp.br/apps/painel-aguas-limpas/painel-aguas-limpas-back.git
> ~~~

> Para alterar a porta de execução, edite a linha correpondente no arquivo ".env.dev".

> #### Executando o projeto (com docker)
> No terminal, acesse o diretório e execute o comando:
> ~~~
> sudo docker-compose up -d --build
> ~~~
> Requer ter iniciado o container docker com o banco de dados
> ()
> 
> Acesse: http://localhost:n_porta_definida

## Documentação 

Com a biblioteca Flask-Swagger, o endpoint padrão para acessar a documentação gerada pelo Swagger é /apidocs. Portanto, para visualizar a documentação, você deve acessar o seguinte URL:

```
http://.../apidocs/
```