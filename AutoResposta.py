import random
import sys

respostas = ["Não", "Sim", "Deveria", "Sei lá", "Acho que não", "Com certeza",
             "Provavelmente", "Não sei", "Acho que sim", "Com certeza não", "Óbvio que não", "Óbvio que sim"]

def perguntar():
    usuario_responde = int(input("Digite 1 caso queira refazer sua pergunta. "))
    if usuario_responde == 1:
       pergunta = input("O que você quer perguntar para o PC?: ")
       responder()
    else: 
        sys.exit()

def responder():
    i = random.randint(0, len(respostas)-1)
    print(respostas[i])
    perguntar()

pergunta = input("O que você quer perguntar para o PC?: ")
responder()