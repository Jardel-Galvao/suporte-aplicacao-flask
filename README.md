<h1 align="center">Aplicação controle de encaminhamentos incorretos - Flask</h1>

<h2 align="center">Resumo da aplicação</h2>
Essa aplicação foi desenvolvida para estudo do desenvolvimento de aplicações Flask. Se trata de uma aplicação para controle de uma meta para uma equipe de suporte, essa meta controla a porcentagem de atendimentos que a equipe de suporte solicita apoio de equipes terceiras sem necessidade, seja porque o suporte deveria ter determinado conhecimento ou já possuí ferramentas necessárias para analisar o caso.

<h2 align="center">Telas da aplicação</h2>

<b>1ª Registro </b>- Nessa tela poderá ser cadastrado o usuário do analista da equipe, aqui são disponibilizadas informações que serão posteriormente utilizadas para relacionar os atendimentos do analista que foram encaminhados de forma incorreta a equipes terceiras.

![teste](https://imgur.com/14StQEx)

<b>2ª Login </b>- A aplicação conta com uma tela de login onde o usuário administrador terá acessos diferentes de um usuário de analista "comum".


<b>3ª Validados </b>- Aqui são listados todos os atendimentos que já passaram por validação do Administrador e serão considerados no cálculo da meta.


<b>4ª Invalidados </b>- Aqui serão listados todos os atendimentos que foram marcados como encaminhamentos incorretos por equipes terceiras, porém, após análise consideramos uma marcação de encaminhamento incorreto inválida.


<b>5ª Encaminhamentos para análise </b>- Aqui serão listados os encaminhamentos feitos pelo técnico atualmente logado na aplicação que foram marcados como encaminhamento incorreto por equipes terceiras, caso o usuário for o Administrador serão listados os atendimentos de todos os analistas.


Nessa tela o analista poderá indicar se concorda ou não para o encaminhamento, caso, sim, o mesmo será direcionado diretamente para a guia de "Validados", caso contrário o mesmo será enviado para a validação do Administrador.


<b>6ª Painel </b>- Nessa tela o usuário administrador irá avaliar os atendimentos pré-avaliado pelos analistas e irá validar ou invalidar o encaminhamento.


<b>7ª Ignorar mês </b>- Nessa tela o usuário administrador poderá para cada analista ignorar os meses nos quais o analista não deve ser considerado na meta, assim o mês informado não será considerado nos cálculos.


<b>8ª Adicionar encaminhamento </b>- Nessa tela o usuário administrador poderá adicionar encaminhamentos incorretos de forma manual, para casos onde as equipes terceiras não marcaram como encaminhamento incorreto, porém o Administrador da meta verificou necessidade.


<b>9ª Backup </b>- Através desse menu é realizado o backup do banco de dados;


<b>10ª Meta </b>- Esse é um menu cascata que contem os seguintes submenus:

<b>Meta encaminhamentos incorretos</b>

Demonstra o percentual de encaminhamentos incorreto para cada analista da equipe em cada mês, também demonstra a média da equipe em cada mês.

<b>Meta encaminhamentos incorretos acumulado</b>

Demonstra o percentual de encaminhamentos incorreto para cada analista da equipe em cada mês acumulado, também demonstra a média da equipe em cada mês.

<b>Quantidade de encaminhamentos total</b>

Lista a quantidade total de encaminhamentos a terceiros para cada analista em cada mês.

<b>Quantidade de encaminhamentos incorretos total</b>

Lista a quantidade total de encaminhamentos incorretos a terceiros para cada analista em cada mês.