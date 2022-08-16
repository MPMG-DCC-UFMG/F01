# Decisões de Projeto

Neste documento registramos as principais decisões de projeto realizadas ao longo das reuniões e na execução das tarefas previstas, tanto na frente de coleta de dados quanto na frente de validação das exigências de transparência. Este documento possui relação com os FAQs criados para [coleta](<FAQ - Coletas.md>) e [validação](<FAQ - Validação.md>).

## Geral

## Coleta
### Siplanweb / Obras Públicas
* **Problema:** Após consultar uma amostra de 13 dos 61 municípios, não foram encontrados dados relativos especificamente aos itens de Obras Públicas.
* **Decisão:** Foi concluído que o template não apresenta dados dessa tag e portanto as coletas não serão realizadas.
* **Observações:** Os dados mais próximos encontrados das exigências da checklist estão na aba de Empenhos, filtrando a pesquisa por Elemento = Obras e instalações. No entanto, as informações encontradas muitas vezes não cumprem os itens exigidos.

### ADPM / Obras Públicas
* **Problema:** Após consultar uma amostra de 10 dos 21 municípios, não foram encontrados dados relativos especificamente aos itens de Obras Públicas.
* **Decisão:** Foi concluído que o template não apresenta dados dessa tag e portanto as coletas não serão realizadas.
* **Observações:** Os dados mais próximos dessa tag estão localizados em documentos relacionados a tag de despesas. No entando, não é possível filtrar apenas as informações relacionadas à Obras Públicas.

### ADPM / Concursos Públicos
* **Problema:** Após consultar uma amostra de 8 dos 21 municípios, não foram encontrados dados relativos especificamente aos itens de Concursos Públicos.
* **Decisão:** Foi concluído que o template não apresenta dados dessa tag e portanto as coletas não serão realizadas.
* **Observações:** Não foram encontrados dados nem mesmo próximos aos especificados pela tag.

### ADPM / Servidores
* **Problema:** Após consultar uma amostra de 8 dos 21 municípios, a coleta de Servidores não se mostrou possível devido a problemas de instabilidade da seção relacionada aos dados relativos a tag em questão. Tal instabilidade reflete em erros de tempo limite excedido nas tentativas de coleta.
* **Decisão:** Foi concluído que não é possível realizar a coleta dos dados relativos a tag Servidores para o template ADPM.
* **Observações:** Tanto a estratégia de coleta estática quanto dinâmica encontraram o mesmo problema durante a execução.

### ADPM / Informações Institucionais do Município
* **Problema:** Após consultar uma amostra de 10 dos 21 municípios, não foram encontrados dados relativos especificamente aos itens de Informações Institucionais.
* **Decisão:** Foi concluído que o template não apresenta dados dessa tag e portanto as coletas não serão realizadas.
* **Observações:** Não foram encontrados dados nem mesmo próximos aos especificados pela tag.

### ABO / Obras Públicas
* **Problema:** Após consultar uma amostra de 10 dos 21 municípios, a coleta de Obras Públicas não se mostrou possível pois os dados requeridos não puderam ser acessados pelos portais de transparência dos municípios. O portal "GeoObras", que contém as informações em questão, não é carregado quando clica-se no link presente nos portais.
* **Decisão:** Foi concluído que não é possível realizar a coleta dos dados relativos a tag Obras Públicas para o template ABO.
* **Observações:** A tag <a> que redirecionaria o usuário ao site GeoObras parece conter um link com protocolo HTTP diferente do usado pelo site.

### PT / Geral
* **Problema:** Foi constatado que o link inicialmente atribuído ao portal da transparência de Conceição da Aparecida na verdade corresponde ao portal de outro município do template PT. Esse fato possivelmente teve relação com uma inclusão equivocada do município de Conceição da Aparecida no cluster do template. Além disso, foi observado que os municípios de Camacho, Itaverava e Santana de Cataguases, que inicialmente não foram associados a nenhum template, possuem portais da transparência com a estrutura do template PT.
* **Decisão:** Foi excluída a participação do município de Conceição da Aparecida no template PT e feita a inclusão dos municípios de Camacho, Itaverava e Santana de Cataguases no mesmo template.
* **Observações:** Foi necessário exluir as coletas de Conceição da Aparecida já realizadas no template PT e aplicar os coletores já desenvolvidos nos município de Camacho, Itaverava e Santana de Cataguases.

## Validação
### Template / Tag / Subtag
* **Problema:**
* **Decisão:** 
* **Observações:**
