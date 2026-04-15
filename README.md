# ScrapBot - Telegram Bot

Bot feito para uso através do Telegram, desenvolvido em Python. Tem como função o scraping automático da página de ofertas do Mercado Livre, assim como a conversão de arquivos XML de notas fiscais em planilhas Excel (Work in Progress).

---

## Funcionalidades

- Scraping de ofertas do Mercado Livre sob demanda

- Envio automático dos produtos encontrados por e-mail em formato .xlsx

- Conversão de arquivos XML (Nota Fiscal) para Excel (em desenvolvimento)

- Sistema de autenticação por senha (em desenvolvimento)

---

## Tecnologias utilizadas

- Python 3.x

- pyTelegramBotAPI (telebot)

- Selenium

- Pandas / openpyxl

- xmltodict

- smtplib

- python-dotenv

---

## Como executar

1. Clone o repositório:

```
git clone https://github.com/HenriqueBXavier/Telegram-Bot-API.git
```

2. Instale as dependências:

```
pip install -r requirements.txt
```

3. Crie um arquivo .env na raiz do projeto com base no .env.example:

```
TELEGRAM_TOKEN=seu_token_aqui
EMAIL_REMETENTE=seu_email@gmail.com
EMAIL_SENHA=sua_senha_de_app
DIR_BASE=caminho/para/diretorio/base
DIR_EXCEL=caminho/para/diretorio/excel
DIR_TEMP=caminho/para/diretorio/temporario
```

4. Execute o bot:

```
python TeleBot.py
```

---

## Estrutura do projeto

```
Telegram-Bot-API/
├── TeleBot.py          # Arquivo principal do bot
├── ScrapMercado.py     # Modulo de scraping do Mercado Livre
├── SepararXML.py       # Modulo de separacao XML
├── requirements.txt    # Dependencias do projeto
├── .env.example        # Exemplo de variaveis de ambiente
└── README.md
```

---

## Observacoes

- O bot solicita autenticacao por senha antes de qualquer operacao

- Emails aceitos: Gmail, Outlook e Hotmail

- O modulo de leitura de XML e a autenticacao estao em desenvolvimento

---

## Autor

Henrique Brazao Xavier

linkedin.com/in/henrique-brazao-xavier

github.com/HenriqueBXavier
