import telepot
import time
import sqlite3
import openpyxl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

# Insira o token do seu bot aqui
token = "6933320373:AAHVNQ_4NQ0VU1rrA9_06ydNR-53cCwUPeI"

# URL do site da PyScript.Tech
url = "https://www.pyscript.tech/"

# ID do Telegram para notificação
telegram_personal_id = 833732395

# Dicionário para armazenar estados dos usuários
user_states = {}

# Mensagem inicial pré-definida
mensagem_inicial = (
    "Olá! Bem-vindo à PyScript.Tech!\n\n"
    f"Para mais informações, visite nosso site: {url}"
)

# Função para inserir um registro de lead no banco de dados
def registrar_lead(user_id, user_name, user_last_name, user_username, interesse, descricao):
    # Cria uma conexão separada para garantir que cada operação ocorra na mesma thread
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            user_name TEXT NOT NULL,
            user_last_name TEXT,
            user_username TEXT,
            interesse TEXT NOT NULL,
            descricao TEXT
        )
    ''')
    conn.commit()

    cursor.execute('''
        INSERT INTO leads (user_id, user_name, user_last_name, user_username, interesse, descricao)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, user_name, user_last_name, user_username, interesse, descricao))
    conn.commit()
    conn.close()

    enviar_mensagem_pessoal(user_name, user_last_name, user_username, interesse, descricao)
    atualizar_planilha(user_name, user_last_name, user_username, interesse, descricao)
    enviar_email()

# Função para enviar mensagem para o Telegram pessoal
def enviar_mensagem_pessoal(user_name, user_last_name, user_username, interesse, descricao):
    mensagem = f"Novo lead:\nNome: {user_name} {user_last_name}\nUsername: {user_username}\nInteresse: {interesse}\nDescrição: {descricao}"
    bot.sendMessage(telegram_personal_id, mensagem)

# Função para atualizar a planilha
def atualizar_planilha(user_name, user_last_name, user_username, interesse, descricao):
    file_path = 'leads.xlsx'
    
    if not os.path.exists(file_path):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(['Nome', 'Sobrenome', 'Username', 'Interesse', 'Descrição'])
    else:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

    sheet.append([user_name, user_last_name, user_username, interesse, descricao])
    workbook.save(file_path)

# Função para enviar a planilha por e-mail
def enviar_email():
    email_user = 'leonardorfragoso@gmail.com'
    email_password = 'ofanteltgansbxju'
    email_send_list = ['leonardorfragoso@gmail.com', 'pyscript.tech@gmail.com']

    subject = 'Novos Leads'

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = ', '.join(email_send_list)
    msg['Subject'] = subject

    body = 'Segue em anexo a planilha atualizada com os novos leads.'
    msg.attach(MIMEText(body, 'plain'))

    filename = 'leads.xlsx'
    attachment = open(filename, 'rb')

    part = MIMEApplication(attachment.read(), Name=filename)
    part['Content-Disposition'] = f'attachment; filename={filename}'
    msg.attach(part)

    attachment.close()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)
    text = msg.as_string()
    server.sendmail(email_user, email_send_list, text)
    server.quit()

# Função para manipular as mensagens recebidas
def handle(msg):
    global user_states

    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type == 'text':
        message_text = msg['text']
        user_id = msg['from']['id']
        user_first_name = msg['from']['first_name']
        user_username = msg['from'].get('username', '')

        # Inicializa o estado do usuário se não existir
        if user_id not in user_states:
            user_states[user_id] = {'state': 'start'}
            
            # Envia a mensagem inicial pré-definida ao usuário
            bot.sendMessage(chat_id, mensagem_inicial)

        state = user_states[user_id]['state']

        if state == 'start':
            if message_text.startswith('/start'):
                bot.sendMessage(chat_id, "Olá! Bem-vindo à PyScript.Tech! Qual é o seu nome?")
                user_states[user_id]['state'] = 'perguntando_nome'

        elif state == 'perguntando_nome':
            user_states[user_id]['user_name'] = message_text
            bot.sendMessage(chat_id, f"Obrigado, {message_text}! Qual é o seu sobrenome?")
            user_states[user_id]['state'] = 'perguntando_sobrenome'


        elif state == 'perguntando_sobrenome':
            user_states[user_id]['user_last_name'] = message_text
            user_name = user_states[user_id]['user_name']
            user_last_name = user_states[user_id]['user_last_name']
            bot.sendMessage(chat_id, f"Perfeito, {user_name} {user_last_name}! Aqui estão alguns dos serviços que oferecemos:")
            bot.sendMessage(chat_id, "1. Desenvolvimento Web\n2. Criação de Bots\n3. Automação com Python\n\nPara mais informações, visite nosso site: " + url)
            bot.sendMessage(chat_id, "Você está interessado em algum serviço específico? (Desenvolvimento Web/Criação de Bots/Automação com Python)")
            user_states[user_id]['state'] = 'confirmando_interesse'

        elif state == 'confirmando_interesse':
            user_states[user_id]['interesse'] = message_text
            bot.sendMessage(chat_id, "Por favor, descreva brevemente sua necessidade:")
            user_states[user_id]['state'] = 'perguntando_descricao'

        elif state == 'perguntando_descricao':
            descricao = message_text
            user_name = user_states[user_id]['user_name']
            user_last_name = user_states[user_id]['user_last_name']
            interesse = user_states[user_id]['interesse']

            registrar_lead(user_id, user_name, user_last_name, user_username, interesse, descricao)
            bot.sendMessage(chat_id, "Obrigado pelo seu interesse! Nossa equipe entrará em contato com você em breve.")
            bot.sendMessage(chat_id, f"Enquanto isso, você pode explorar mais sobre nossos serviços em nosso site: {url}")

            # Reseta o estado do usuário para permitir um novo início
            user_states[user_id]['state'] = 'start'

# Inicia o loop infinito para manter o chatbot em execução
bot = telepot.Bot(token)

print('Bot iniciado, esperando mensagens...')

# Inicia o loop de espera por mensagens
bot.message_loop(handle)

# Mantém o bot em execução
while True:
    time.sleep(10)
