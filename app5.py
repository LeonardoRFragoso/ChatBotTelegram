import telepot
import time
import sqlite3

# Insira o token do seu bot aqui
token = "6933320373:AAHVNQ_4NQ0VU1rrA9_06ydNR-53cCwUPeI"

# URL do serviço
url = "https://pay.kiwify.com.br/MXMKc1H"

# Dicionário para armazenar estados dos usuários
user_states = {}

# Função para inserir um registro de pagamento no banco de dados
def registrar_pagamento(user_id, user_name, user_last_name, user_username, pagamento):
    # Cria uma conexão separada para garantir que cada operação ocorra na mesma thread
    conn = sqlite3.connect('pagamentos.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pagamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            user_name TEXT NOT NULL,
            user_last_name TEXT,
            user_username TEXT,
            pagamento BOOLEAN NOT NULL
        )
    ''')
    conn.commit()

    cursor.execute('''
        INSERT INTO pagamentos (user_id, user_name, user_last_name, user_username, pagamento)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, user_name, user_last_name, user_username, pagamento))
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
                bot.sendMessage(chat_id, "Olá! Antes de continuar, por favor, informe o seu nome :")
                user_states[user_id]['state'] = 'perguntando_nome'

        elif state == 'perguntando_nome':
            user_states[user_id]['user_name'] = message_text
            bot.sendMessage(chat_id, f"Obrigado, {message_text}! Agora, por favor, informe seu sobrenome:")
            user_states[user_id]['state'] = 'perguntando_sobrenome'

        elif state == 'perguntando_sobrenome':
            user_states[user_id]['user_last_name'] = message_text
            user_name = user_states[user_id]['user_name']
            user_last_name = user_states[user_id]['user_last_name']
            bot.sendMessage(chat_id, f"Perfeito, {user_name} {user_last_name}! Clique no link abaixo para realizar o pagamento: {url}")
            bot.sendMessage(chat_id, "Você realizou o pagamento? (sim/não)")
            user_states[user_id]['state'] = 'confirmando_pagamento'

        elif state == 'confirmando_pagamento':
            payment_confirmation = message_text.lower()
            
            user_name = user_states[user_id]['user_name']
            user_last_name = user_states[user_id]['user_last_name']

            if payment_confirmation in ['sim', 'yes']:
                registrar_pagamento(user_id, user_name, user_last_name, user_username, True)
                bot.sendMessage(chat_id, "Pagamento confirmado! Obrigado.")
            else:
                registrar_pagamento(user_id, user_name, user_last_name, user_username, False)
                bot.sendMessage(chat_id, "Pagamento não confirmado. Se precisar de ajuda, entre em contato conosco.")

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
