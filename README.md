# Telegram-Bot-API

Essa pasta foi criada para o aprendizado da linguagem python e seus recursos.
Neste arquivo é possivel perceber a evolução dos códigos a partir do teste.py, nesse código, utiliza-se dos imports: Datetime e pandas para a edição das tabelas criadas,
consequentemente utilizada no programa Telebot.py para melhor identação dos arquivos.

O maior código (ScrapMercado) consiste em uma consulta utilizando o selenium. O código abre a página de ofertas do mercado livre e escreve os itens das paginas em um arquivo .xlsx,
até o valor limite (varia entre 19 e 21 páginas) ou até o limitador atingir o valor selecionado.

SepararXML consiste em um programa (não muito dinâmico até entao) que recebe um documento XML e separa informações úteis para análise,
o programa retorna os itens em uma tabela criada pelo Pandas e o envia para o email escolhido (caso esteja sendo utilizado pelo Telebot).
