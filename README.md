# F01
Processamento dos dados coletados dos portais de transparência dos municípios do Estado de Minas Gerais

Este repositório apresenta códigos dos validadores e da API que disponibiliza os resultados

O repositório está dividido nos seguintes diretórios:

* src: contém implementações dos validaores, referentes as licitações públicas;
* service: contém o código da API REST JSON que disponibiliza os resultados obtidos para cada município;


## API

### Iniciar a API localmente 
A primeira etapa para poder instalar o sistema é realizar o donwload de seu código-fonte. Para isso, utilize as ferramentas do GitHub para baixar o repositório localmente. Em seguida, é necessário um virtualenv ou uma máquina apenas com Python 3.7+ com requirements descritos em "requirements.txt"

Dentro de /service rode o comando:

<!-- export FLASK_ENV=development -->
```
FLASK_APP=main.py flask run
```

Por padrão a porta será a `5000` http://localhost:5000

## Consultas ao resultado dos validadores

Obs: Os itens estão listados em 'lista_exigencias.csv'

### Consulta de todos os itens de um municipio:

```
http://localhost:5013/api/{municipio}
```
- Método GET

- Entrada: 
    ID do municipio (código IBGE).

- Resposta: Formato `JSON` com a resposta de todos os itens (possívelmente de 1 até 124).

### Consulta a um item específico de um municipio:

```
http://localhost:5013/api/{municipio}/{nº_do_item}
```
- Método GET

- Entrada - Parâmetros: 
 1) ID do municipio (código IBGE)
 2) O número do item, algum dos listados em 'lista_exigencias.csv'.

- Resposta: Formato `JSON` com a resposta do item específico.


### Resposta de um item:

A resposta JSON de um item tem dois campos: 'codigo' e 'justificativa'.

    - Códigos respectivos a coleta:

    * código: ISSUE_BLOQUEADA, justificativa: "Issue bloqueada por algum motivo"
    * código: NAO_COLETAVEL_REDIRECIONADO, justificativa: = "Dados são encontrados somente fora do padrão do template"
    * código: NAO_COLETAVEL_TIMEOUT, justificativa: = "Dados não coletados devido a erro de Timeout"
    * código: NAO_LOCALIZADO, justificativa: = "Dados não foram localizados no template"
    * código: NAO_LOCALIZADO_LINK_INCORRETO, justificativa: = "Dados inacessíveis pelos portais do template"

    - Códigos respectivos a validação:

    * código: ITEM_NAO_DISPONIVEL, justificativa: "Item ainda não validado"
    * código: FALSE, justificativa: "Validação informou que o item coletado nao atende aos requisitos"
    * código: TRUE, justificativa: "Item validado com sucesso"

    - Códigos respectivos a outros erros:

   * código: MUNICIPIO_NAO_DISPONIVEL, justificativa: "Municipio inválido ou não abordado"

### Exemplo:

- Requisição:

```
http://localhost:5013/api/3143906/7 // (Município Muriaé, item 7 (Link de respostas a perguntas mais frequentes da sociedade.))
```

- Resposta:

```
{
  "7": {
    "codigo_resposta": "TRUE", 
    "justificativa": "Item validado com sucesso. Explain - Quantidade de arquivos analizados: 5. Quantidade de aquivos que possuem referência a Perguntas Frequentes: 5"
  }
}
```