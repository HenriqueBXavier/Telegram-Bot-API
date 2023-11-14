#1 Importar Bibliotecas Necessárias

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
from tabulate import tabulate
import keyboard

# Ler planilha contendo os números de telefone dentro do Excel (arquivo xlsx)
contatos_df = pd.read_excel("Enviar.xlsx")
# print(tabulate(contatos_df, headers='keys', tablefmt='psql')) # Opcional - Mostra no código a tabela

# Abre o chrome.
navegador = webdriver.Chrome()
navegador.get("https://web.whatsapp.com/")

# Verifica se a pagina web do wpp carregou completamente
while len(navegador.find_elements("id",'pane-side')) < 1:
    time.sleep(3)

""" 
 Pega os dados da tabela excel inseridas aqui na variável CONTATOS_DF
 Para cada linha da tabela, é inserido um número na var I,
 Para cada coluna da tabela, é necessário filtrar pelo nome da coluna, obtendo a localização do cabeçalho
 Juntando a linha (i) com o valor localizado com o comando contatos_df.loc[] é possivel obter a linha e colunha dinamicamente.
"""

for i, mensagem in enumerate(contatos_df['Mensagem']):
    pessoa = contatos_df.loc[i, "Pessoa"]
    numero = contatos_df.loc[i, "Número"]
    texto = urllib.parse.quote(f"eita, {pessoa}!! {mensagem}")
    link = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"
    navegador.get(link)

    #Enquanto dentro do link sugerido não for encontrado o elemento pane-side, espere.
    while len(navegador.find_elements("id",'pane-side')) < 1:
        time.sleep(5)

    # Se o elemento sugerido for maior do que 1 (existir), prossiga.
    if len(navegador.find_elements("xpath", '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]')) < 1:
        # Procura pelo elemento XPATH da barra de mensagem do wpp, e então, ele escreve a mensagem e envia utilizando o import Keys do Selenium
        navegador.find_element("xpath", '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p').send_keys(Keys.ENTER)
        # Dentro do elemento sugerido, pressione ENTER.
        time.sleep(12)


    

#//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p inserçao de texto
#//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1] texto de erro

#//*//p[@class='promotion-item__title']
#//span[@class='andes-pagination__arrow-title' and text()='Próxima']