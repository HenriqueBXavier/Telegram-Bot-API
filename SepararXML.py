import xmltodict
import os
import json
import openpyxl
import pandas as pd


diretorio = "C:\\Users\\Lisianto\\Desktop\\piu piu utilizas\\"
dir_excel = "A:\\piupiu produtos\\"

def Conversor(arquivo, itens):
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

colunas = ["Numero da Nota", "Empresa Emissora", "Nome do Cliente", "Endereço do Destinatário", "Peso"]
itens = []

lista_arq = os.listdir(diretorio)

for arquivo in lista_arq:
    Conversor(arquivo, itens)

tabela = pd.DataFrame(columns=colunas, data=itens)
tabela.to_excel(f"{dir_excel}NotasFiscais.xlsx", index=False)

