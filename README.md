# F01
Processamento dos dados coletados dos portais de transparência dos municípios do Estado de Minas Gerais

Este repositório apresenta códigos dos validadores e da API REST JSON que disponibiliza os resultados.


## API de Consultas aos Resultados dos Validadores

### Iniciar a API localmente 
A primeira etapa para poder instalar o sistema é realizar o donwload de seu código-fonte. Para isso, utilize as ferramentas do GitHub para baixar o repositório localmente. Em seguida, é necessário um virtualenv ou uma máquina apenas com Python 3.7+ com requirements descritos em "requirements.txt"

Dentro de /service rode o comando:

<!-- export FLASK_ENV=development -->
```
FLASK_APP=main.py flask run
```

A porta adotada será a `5013` http://localhost:5013

Obs: Os itens estão listados em ['lista_exigencias.csv'](https://github.com/MPMG-DCC-UFMG/F01/blob/main/service/src/checklist/lista_exigencias.csv)

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

## Resposta de um item

A resposta JSON de um item possui dois campos: 'codigo' e 'justificativa', conforme a seguir:

| codigo | justificativa | contexto |
| - | - | - |
| `ISSUE_BLOQUEADA` | "Issue bloqueada por algum motivo" | Coleta |
| `NAO_COLETAVEL_REDIRECIONADO` | "Dados são encontrados somente fora do padrão do template" | Coleta |
| `NAO_COLETAVEL_TIMEOUT` | "Dados não coletados devido a erro de Timeout" | Coleta |
| `NAO_LOCALIZADO` | "Dados não foram localizados no template" | Coleta |
| `NAO_LOCALIZADO_LINK_INCORRETO` | "Dados inacessíveis pelos portais do template" | Coleta |
| `MUNICIPIO_NAO_DISPONIVEL` | "Municipio inválido ou não abordado" | API | 
| `ITEM_NAO_DISPONIVEL` | "Item ainda não validado" | Validação | 
| `ERRO_VALIDADO` | "Validação informou que o item coletado nao atende aos requisitos" | Validação | 
| `OK_VALIDADO` | "Item validado com sucesso" | Validação | 
 
 
É importante destacar que, no caso da resposta ser `OK_VALIDADO` ou `ERRO_VALIDADO` (respostas da fase de validação) a justificativa poderá variar, apresentando uma explicação específica sobre a validação do item solicitado. 

Para facilitar o entendimento dos respectivos códigos de resposta, adicionamos a coluna "contexto" à tabela anterior, já que cada resposta é associada à uma fase específica da verificação automática de normativas. Em geral, ou o contexto da resposta refere-se a fase de coleta (não se chegou a fase de validação) ou à fase de validação. Não há campo "contexto" na resposta devolvida.

## Exemplo

- Requisição (Município Muriaé, item 7 (Link de respostas a perguntas mais frequentes da sociedade.):

```
http://localhost:5013/api/3143906/7 
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
