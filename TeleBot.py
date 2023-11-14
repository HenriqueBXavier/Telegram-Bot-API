# Telegram API
import telebot
from telebot import types

# Imports para conversão XML

import xmltodict
import os
import json
import openpyxl
import pandas as pd

# Imports para trabalho com tempo e timers
import time
from datetime import datetime
from datetime import date

# Imports para trabalho com emails

import re

# Inicialização de variáveis globais

global gethora, getdia, logged

# Variavel para verificação de senha
logged = False

# Variaveis de diretório
diretorio = "C:\\Users\\Lisianto\\Desktop\\piu piu utilizas\\"
dir_excel = "D:\\piupiu produtos\\"
dir_temp = "D:\\tempy"

# Basicamente um bloco de código para transformar a hora em int e usar nos outros blocos de código
gethora = datetime.now()
horaint = gethora.strftime("%H")
horaint = int(horaint)
getdia = date.today()
dia_polido = getdia.strftime("%d_%M")

# Chave do bot
chave_api_tel = "5839791784:AAHQL_i9WxgFIqOZ_ju3MO61KegwsY81pk4"
bot = telebot.TeleBot(chave_api_tel)

# Começo do código do bot, inicialização.

@bot.message_handler(commands=['start', 'reset'])
def Login(msg): # Login -> Ativada no começo do código, pergunta a senha e então redireciona o usuário para o próximo passo
    
    logged = False
    bot.reply_to(msg, "Olá, digite sua senha: ")
    bot.register_next_step_handler(msg, check_senha)

def check_senha(msg): # Check Senha -> Confere se a senha digitada é a senha correta para login 
    global logged
    if msg.text != '1192':
        bot.reply_to(msg, "Senha errada, tente novamente")
        Login(msg)
    else:
        logged = True
        Bem_Vindo(msg) 

def Bem_Vindo(msg): # Bem Vindo -> Mensagem de boas vindas após completar o login.

    # Verificar login
    global logged
    if logged == False:
        return

    texto = "aqui é o ScrapBot.\nO que deseja?"

    if horaint >= 6 and horaint <= 11:
        bot.reply_to(msg, f"Bom dia, {texto}")

    elif horaint >= 12 and horaint <= 17:
        bot.reply_to(msg, f"Boa tarde, {texto}" )
        
    elif horaint >= 18 or horaint <= 5:
        bot.reply_to(msg, f"Boa noite, {texto}")
    
    Perguntar_Func(msg)

# Declaração do Uso do Bot

def Perguntar_Func(msg): # Perguntar Rasp -> Pergunta se o usuário deseja saber as ultimas ofertas do Mercado Livre

    # Verificar login
    global logged
    if logged == False:
        return

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Verificar Ofertas (Mercado Livre)', 'Enviar Nota Fiscal (XML)', 'Voltar')
    bot.send_message(msg.chat.id, "Selecione uma opção: ", reply_markup=markup)
    bot.register_next_step_handler(msg, processar_resp)
    
def processar_resp(msg): # Processar Resp -> Alterna entre as repostas do usuário para redirecionar o mesmo em relação á resposta

    if msg.text == 'Verificar Ofertas (Mercado Livre)':

        bot.send_message(msg.chat.id, "Entendido, iniciando sessão...")
        Perguntar_Email(msg)

    elif msg.text == 'Enviar Nota Fiscal (XML)':

        bot.send_message(msg.chat.id, "Entendido, iniciando sessão...")
        Alocar_Doc(msg)

    elif msg.text == 'Voltar':
        bot.send_message(msg.chat.id, "Entendido, reiniciando...")
        Perguntar_Func(msg)
    
    else:
        bot.send_message(msg.chat.id, "Escolha uma das opções apresentadas.\nPor favor, tente novamente.")
        Perguntar_Func(msg)

# Scrap do Mercado Livre

def Perguntar_Email(msg): # Perguntar Email -> Pergunta ao usuário quais serão os emails para enviar a raspagem
    # Verificar login
    global logged
    if logged == False:
        return

    bot.send_message(msg.chat.id, "Digite um email válido para receber o arquivo, em caso de múltiplos emails, utilize a virgula para separa-los: ")
    bot.register_next_step_handler(msg, Alocar_Email)
    
def Alocar_Email(msg):# Alocar Email -> tem como função fiscalizar o email inserido pelo usuário e integrar o email na class thrashing de ScrapMercado
    
    emails = msg.text.split(',')
    emailrange = len(emails)

    emails_validos = []

    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    for email in emails:

        if re.match(padrao, email.strip()) and ('gmail.com' in email.strip() or 'outlook.com' in email.strip() or 'hotmail.com' in email.strip()):
        
            emails_validos.append(email.strip())
            
        else:
            bot.send_message(msg.chat.id, f'Email inválido: {email.strip()}')
            Perguntar_Email(msg)

    if len(emails_validos) == emailrange:

        bot.send_message(msg.chat.id, F'Emails válidos, prosseguindo...')
        from ScrapMercado import thrashing

        inicio = thrashing()
        inicio.iniciar(emails_validos) # Passa o email para o método receber_enviar_email da classe thrashing
        
        bot.send_message(msg.chat.id, f"O email contendo o item chegará em alguns minutos. \nReiniciando...")

        Login(msg)

# Transformar arquivos XML

def Alocar_Doc(msg): # Alocar Documento -> Pede ao usuário um documento para conversão

    bot.send_message(msg.chat.id, "Preciso que você envie um arquivo XML para que possamos converte-lô em um arquivo excel.")
    bot.register_next_step_handler(msg, Verif_XML)

@bot.message_handler(content_types=['document'])
def Verif_XML(msg): # Verificar se a próxima mensagem enviada é um Arquivo
    
    if msg.document:

        info_arq = bot.get_file(msg.document.file_id)
        nome_arq = msg.document.file_name

        baixar = bot.download_file(info_arq.file_path)

        with open(os.path.join(dir_temp, nome_arq), 'wb') as novo_arq:
            novo_arq.write(baixar)

        processar_arq(nome_arq, msg.chat.id)

    else:
    
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Sim', 'Não')
        bot.send_message(msg.chat.id, "Arquivo não identificado, ainda deseja realizar uma conversão?", reply_markup=markup)
        bot.register_next_step_handler(msg, verif_resp_XML)

def verif_resp_XML(msg): # Verificar se o usuário ainda quer utilizar o bot

    if msg.text == 'Sim':

        bot.send_message(msg.chat.id, "Entendido, tente novamente.")
        Alocar_Doc(msg)

    elif msg.text == 'Não':

        bot.send_message(msg.chat.id, "Entendido, reiniciando...")
        Login(msg)

def processar_arq(arquivo, chat_id): # Processamento e extração de informações do arquivo
    
    itens = []
    Conversor(arquivo, itens)

   
    colunas = ["Numero da Nota", "Empresa Emissora", "Nome do Cliente", "Endereço do Destinatário", "Peso"]
    tabela = pd.DataFrame(columns=colunas, data=itens)

    cam_arq_excel = f"{dir_excel}NotasFiscais.xlsx"
    tabela.to_excel(cam_arq_excel, index=False)

    with open(cam_arq_excel, 'rb') as file:
        bot.send_document(chat_id, file)

    os.remove(cam_arq_excel)
    os.remove(os.path.join(dir_temp, arquivo))

def Conversor(arquivo, itens): # Conversor para criação do arquivo XML

    print(f"\033[32mArquivo resgatado:\033[0m \033[34m{arquivo}\033[0m")

    with open(f'{diretorio}{arquivo}', "rb") as arquivo_xml:

        #Conversão de XML para Dicionário Python
        arq_dict = xmltodict.parse(arquivo_xml)

        try:
            if "NFe" in arq_dict:
                inform_nota = arq_dict["NFe"]["infNFe"]
            else:
                inform_nota = arq_dict["nfeProc"]["NFe"]["infNFe"]
            
            numero_nota = inform_nota["@Id"]
            empresa_emissora = inform_nota["emit"]["xNome"]
            empresa_dest = inform_nota["dest"]["xNome"]
            endereco_dest = inform_nota["dest"]["enderDest"]
            if 'vol' in inform_nota["transp"]:
                peso = inform_nota["transp"]["vol"]["pesoB"]
            else:
                peso = "Não identificado"
            itens.append([numero_nota, empresa_emissora, empresa_dest, endereco_dest, peso])
            
            
        except Exception as e:
            print(e)
            print(json.dumps(arq_dict, indent=4))

# Em construção



bot.polling()


    
