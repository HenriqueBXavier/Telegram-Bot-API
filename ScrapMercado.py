# Imports para trabalho com datas e horários 
import time
from datetime import datetime, date
from datetime import timedelta

# Imports do Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import OS
import os

# Imports para recebimento de emails
import smtplib
import email.message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders

# Imports para criação de planilhas excel
import openpyxl

class thrashing:

    def iniciar(self, email_validos): # Inicialização dos métodos essenciais para o código, sujeito á aumento de métodos.

        self.ajustar_e_abrir_chromepage()

        self.start_time = time.time()
        self.email = email_validos
        self.localizar_elementos()
        self.exportar_itens_excel()
        self.receber_enviar_email()

    def ajustar_e_abrir_chromepage(self): # Inicia o navegador

        # Ajustes de acordo com a necessidade do código, variando á permissões para o uso de senhas até desabilitação de notificações.
        self.navegador = webdriver.Chrome()
        self.navegador.maximize_window()
    
        self.navegador.get("https://www.mercadolivre.com.br/ofertas") # Abre o navegador
        time.sleep(5)

        self.cookie = self.navegador.find_element("xpath", "//button[@type='button' and text()='Aceitar cookies']") # Procura e fecha a notificação de permissão para uso de cookies
        self.cookie.click()
        print("\033[33mIniciando scaneamento.\033[0m")

    def localizar_elementos(self): # Inicia a raspagem de dados

        limitador = 2
        pagat = 0

        # Definição das listas
        self.lista_de_itens = []
        self.lista_de_precos = []
        self.antiga_lista_de_precos = []

        while True: # Enquanto o navegador puder achar os elementos, o código continuará a rodar.

            elemento_nomes = self.navegador.find_elements("xpath","//p[@class='promotion-item__title']")
            elemento_precos = self.navegador.find_elements("xpath", "//span[@class='andes-money-amount__fraction' and text()]")
        
            alternador = 2
            for elemento_nome in elemento_nomes:
                self.lista_de_itens.append(elemento_nome.text) # Insere o nome do item na lista

            # Para cada item nas listas, ele fará o alternador aumentar de 1 em 1,
            # Assim, o alternador decidirá o que é o preço antigo e qual é o desconto.

            for elemento_preco in elemento_precos:
                if alternador % 2 == 0:
                    
                    self.lista_de_precos.append(elemento_preco.text) # Insere o desconto na lista
                else :
                    self.antiga_lista_de_precos.append(elemento_preco.text) # Insere o preço anterior na lista
                    
           
                alternador += 1

            try:
                    # Procura o botão Próximo na aba do navegador
                    btn_proximo = self.navegador.find_elements("xpath", "//span[@class='andes-pagination__arrow-title' and text()='Próxima']")
                    print("\033[33mNavegando para a próxima página... \033[0m")
                    btn_proximo[0].click()
                    # Manda o navegador esperar 10s após clickar no botão, até que o elemento que define o nome dos itens seja carregado novamente
                    WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//p[@class='promotion-item__title']")))
                    # E então o código acima volta a rodar
                    pagat += 1

                    if pagat == limitador:
                        break

            # Exceções caso o código não possa achar ou interagir com os elementos anteriores.
            except ElementNotInteractableException: 

                print("\033[33mEscaneamento finalizado.\033[0m")
                break
            except NoSuchElementException:

                print("\033[33mEscaneamento finalizado.\033[0m")
                break
        
        self.navegador.quit()

    def exportar_itens_excel(self): # Inicia a criação dos arquivos Excel (.xlsx)
        
        definir_horario_scrap = datetime.now()
        hora = definir_horario_scrap.strftime("%H_%M") # Transforma o horário de execução em variável

        definir_dia_scrap = date.today()
        data = definir_dia_scrap.strftime("%d_%m") # O dia da execução em variável

        global tab_raspagem # Criação de variável global para uso nos próximos itens
        tab_raspagem = f"Raspagem{data}as{hora}.xlsx" # Mescla ambos, criando um string com a especificação do arquivo Excel

        global caminho_arq
        caminho_arq = fr'D:\piupiu produtos\{tab_raspagem}' # Redefine o caminho do arquivo

        wb = openpyxl.Workbook() # Cria o arquivo excel
        sheet = wb.active # Cria uma planilha

        cabecalho = ['Itens', 'Preços', 'Preço Antigo'] # Define o cabeçalho
        sheet.append(cabecalho)

        # Para cada item nas listas anteriores, ele juntará os itens respectivamente, seguindo: Item, Preço, Preço Anterior, utilizando a função in zip
        for item, preco, antigo_preco in zip(self.lista_de_itens, self.lista_de_precos, self.antiga_lista_de_precos):

            linha = [item, preco, antigo_preco]
            sheet.append(linha) # Mescla os itens e os coloca em uma linha no excel

        sheet.column_dimensions['A'].width = 100

        wb.save(caminho_arq) # Salva e renomeia o arquivo

        end_time = time.time()
        self.execution_time = end_time - self.start_time

        
        # Cálculo do tempo de execução
        execution_time = end_time - self.start_time

        # Converter para objeto timedelta
        minutes, seconds = divmod(execution_time, 60)

        # Criar objeto timedelta
        delta = timedelta(minutes=minutes, seconds=seconds)

        # Formatar o tempo de execução
        formatted_time = "{:02d}:{:06.3f}".format(int(minutes), seconds)


        # Exibir o tempo de execução
        print(f"Tempo de execução: \033[95m{formatted_time}\033[00m")

    def receber_enviar_email(self):
            
        cam_arqui = f'D:\piupiu produtos\{tab_raspagem}'

        # Definição do Remetente, Destinatário, assunto e senha do email

        Assunto = 'Referente ás ofertas do Mercado Livre'
        Remetente = 'testescrap35@gmail.com'
        password = 'puohllgpeakocvxl'

        corpo = """
        Não responda essa mensagem.
        Mensagem automatica enviada pelo ScrapBot
        """

        servidor_smtp = "smtp.gmail.com"
        porta_smtp = 587

        for Destinatario in self.email:

            # Adicionar o corpo do e-mail

            mensagem = MIMEMultipart()
            mensagem['Subject'] = Assunto
            mensagem['From'] = Remetente
            mensagem['To'] = Destinatario
            mensagem.attach(MIMEText(corpo, 'plain'))

            
            # Adicionar o anexo ao e-mail
            with open(cam_arqui, "rb") as attachment:
                anexo = MIMEApplication(attachment.read(), _subtype="xlsx") 
                anexo.add_header('Content-Disposition', 'attachment', filename=tab_raspagem)
                mensagem.attach(anexo)

            # Iniciar a conexão com o servidor SMTP
            server = smtplib.SMTP(servidor_smtp, porta_smtp)
            server.starttls()

            server.login(Remetente, password)

            server.sendmail(Remetente, Destinatario, mensagem.as_string())

            server.quit()

            
        os.remove(cam_arqui)
        
        #   XPath para rastreamento de elementos especificos 
        #   //span[@class='andes-money-amount__fraction' and text()] -> Preço dos itens
        #   //span[@class='andes-pagination__arrow-title' and text()='Próxima']) -> Botão próximo
        #   //p[@class='promotion-item__title'] -> Nomes do itens


#inicio = thrashing()
#inicio.iniciar(email) # Dá inicio ao código
#inicio.receber_enviar_email()