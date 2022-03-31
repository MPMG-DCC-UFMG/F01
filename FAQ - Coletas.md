# Coletas - FAQ


## Estou coletando os dados necessários para avaliar o item??

> Ex: "Estou com uma dúvida com relação ao grau de tolerância dos erros que encontramos! Por exemplo: Na coleta geral de Divinópolis, foi registrado ERROR em 7 linhas. Pelo que interpretei, dessas 7 linhas, 5 se referem a páginas "quebradas" e 2 se referem a páginas que podem ser acessadas normalmente!"

A [checklist](https://docs.google.com/spreadsheets/d/1ppFLGORKQBPDdtN2B41QPwq9NQXApGBS68N87L1u2qE/edit#gid=946093093) é um recurso que vocês temos para avaliar isso. Basicamente, nós precisamos dos dados que são necessário para avaliar um item. Por exemplo, suponhamos que você esteja coletando os dados necessários para avaliar um item da checklist que é a *"Aba denominada 'Transparência' no menu principal do site"*, um possível erro crítico seria quando não é possível carregar o menu principal do site. Agora, todos os erros que não influenciam a coleta correta desse dado podem sim ser desconsidarados.

Com esse item é facil julgar, mas, por exemplo, na coleta geral dos dados do portal transparência, esperamos um pouco mais da coleta, isto é, não queremos apenas o cabeçalho. Sempre que houver essas dúvidas pensem na checklist. 


## Depois que criamos o coletor no MP ele "roda sozinho"? Porque a opção de detalhes não aparece!

Arraste a barra pra direita. Alguns coletores possuem uma URL gigantesca. Isso acaba mandando o detalhes muito para a direita.


## Há algum procedimento padrão para o erro "Web Page Blocked"?
<!-- <img src="https://cdn.discordapp.com/attachments/894938897392476191/904743808791617578/unknown.png" title="" alt="" data-align="center"> -->
Sim! Esse erro é gerado pois o site possui um mecanismo que detecta robô. Para contornar esse mecanismo, você pode ativar a ferramenta que muda o *user agent*. Basta ativá-la e colocar para mudar user agent a cada 1 request.  Atualmente, esse recurso só funciona para coletas estáticas.


## Quando acionamos o "salvar página" com o download de arquivos ligado, o coletor baixa os arquivos linkados na página. É isso mesmo?
Sim. Porém, se o seu interesse é apenas baixar os arquivos de uma determinada página, não é necessário colocar a ação salvar página.

## O que fazer quando o site que o coletor abre é diferente daquele acessado manualmente, sendo que é a mesma url?

Screeshot do Coletor

![](https://cdn.discordapp.com/attachments/894938897392476191/902904836671037470/Captura_de_ecra_de_2021-10-27_10-00-20.png)

Site que eu vejo ao acessar manualmente:

![](https://cdn.discordapp.com/attachments/894938897392476191/902904941159530536/Captura_de_ecra_de_2021-10-27_10-01-38.png)

R.: O pyppeteer mantem sempre a mesma resolução de 800x600. Dependendo da resolução o fullxpath pode mudar. Se você inspecionar o elemento vai ter esse simbolo  da imagem:

<img src="https://cdn.discordapp.com/attachments/894938897392476191/902905480798674964/unknown.png" title="" alt="" data-align="center">

Clique nele e voce vai ser direcionado para um menu de responsividade. Nesse menu você pode alterar pra resolução que você quer e obter os fullxpath certo do html.

## Eu tive a impressão de que as coletas deveriam partir da página principal! Mas então posso partir de qualquer página?
Sim, pode partir de onde for mais fácil.

## Como q funciona o abrir em nova aba? Todo comando q eu colocar a partir dai sera nela?
Sim.

<!-- ## Pessoal, nessas coletas dinâmicas, eu tenho q deixar baixar arquivos ativado msm ne? Ou o clique no link ja é suficiente? -->


## Estou recebendo erro de sintaxe inválida com o xpath "//*[@class="container col two"]". Não estou entendendo o porquê.
Tente tirar o aspas duplas do meio e colocar aspas simples.

Trocar isso -> `"//*[@class="container col two"]"`   por isso ->  `"//*[@class='container col two']"`

## Se, por exemplo, obtemos erro com uma única página da coleta que não compromete o restante e essa página não é importante para a checklist, o ideal é contornar o erro de alguma forma? Ou podemos fazer a coleta no MP mesmo assim?
Pode fazer a coleta no MP.

## Nos municipios que ja existem a pasta, devo colocar o mesmo caminho?
Sim.

## Só precisamos considerar o erro de Traceback?
Esses são os erros que fazem o coletor fechar.


## Erro: `File "/home/arthur/iniciacao/C01/crawlers/base_spider.py", line 222, in store_html`
Se for uma coleta estática, sim. Se for dinâmica, talvez.  Acesse os detalhes do coletor e cliqeu em "mais detalhes". Há duas opções, escolha "automático."

## Uma coleta que configurei não deu erros, mas apenas um warning. É uma coleta simples de páginas que podem ser acessadas a partir do portal da prefeitura! Nesse caso posso considerar ela bem sucedida?
Se coletou, está ok.



