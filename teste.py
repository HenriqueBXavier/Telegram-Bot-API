from datetime import datetime
from datetime import date
import pandas as pd
import openpyxl


definir_horario_scrap =  datetime.now()
hora = definir_horario_scrap.strftime("%H_%M")
definir_dia_scrap = date.today()
data = definir_dia_scrap.strftime("%d_%m")

definir_nome_tab = f"Raspagem{data}as{hora}.xlsx"

dados = [
    {'Frutas': 'Maçã', 'Preço': 2.5, 'Quantidade': 10},
    {'Frutas': 'Banana', 'Preço': 1.5, 'Quantidade': 20},
    {'Frutas': 'Laranja', 'Preço': 3.0, 'Quantidade': 15}
]

# Criar um DataFrame a partir dos dados
df = pd.DataFrame(dados)

# Criar o arquivo Excel
nome_arquivo = 'frutas.xlsx'
df.to_excel(nome_arquivo, index=False)

# Ler o arquivo Excel com o cabeçalho
df_com_cabecalho = pd.read_excel(nome_arquivo)

# Exibir o DataFrame com o cabeçalho
print(df_com_cabecalho)