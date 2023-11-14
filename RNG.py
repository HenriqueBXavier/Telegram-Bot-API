import random, sys

x = 1
y = 6

rng = random.randint(x,y)
print(rng)

def retry():
    num1 = int(input(f"Escolha um número de {x} a {y}: "))
    rng = random.randint(x,y)
    decisao(rng, num1)

def escolha():
    escolha = int(input(f"\033[31mVocê errou, digite 1 se quiser jogar novamente. \033[0m"))
    if escolha == 1:
        return retry()
    else:
        sys.exit

def vencedor():
    vitoria = int(input("\033[32mVocê venceu, digite 1 se quiser jogar novamente. \033[0m"))
    if vitoria == 1:
        return retry()
    else:
        sys.exit

num1 = int(input(f"Escolha um número de {x} a {y}: "))

def decisao(rng, num1):
    if rng == num1:
        print(f"Número escolhido: \033[32m{num1}\033[0m, Número gerado: \033[32m{rng}\033[0m")
        return vencedor()
    else:    
        print(f"Número escolhido: \033[33m{num1}\033[0m, Número gerado: \033[31m{rng}\033[0m")
        return escolha()
    
decisao(rng, num1)