import telepot
import time
import sqlite3

# Insira o token do seu bot aqui
token = "6933320373:AAHVNQ_4NQ0VU1rrA9_06ydNR-53cCwUPeI"

# URL do site da PyScript.Tech
url = "https://www.pyscript.tech/"

# Dicionário para armazenar estados dos usuários
user_states = {}

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
