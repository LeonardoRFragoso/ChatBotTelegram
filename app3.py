import telepot
import time

# Insira o token do seu bot aqui
token = "6933320373:AAHVNQ_4NQ0VU1rrA9_06ydNR-53cCwUPeI"

# URL do serviço
url = "https://pay.kiwify.com.br/MXMKc1H"

# Dicionário para armazenar os estados dos usuários
user_states = {}

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        message_text = msg['text']
        user_id = msg['from']['id']
        user_name = msg['from']['first_name']

        if user_id not in user_states:
            user_states[user_id] = {'state': 'start'}

        user_state = user_states[user_id]['state']

        if message_text.startswith('/start') or user_state == 'start':
            bot.sendMessage(chat_id, f"Olá {user_name}! Qual é o seu nome completo?")
            user_states[user_id]['state'] = 'name'

        elif user_state == 'name':
            user_states[user_id]['name'] = message_text
            bot.sendMessage(chat_id, "Qual é o seu e-mail?")
            user_states[user_id]['state'] = 'email'

        elif user_state == 'email':
            user_states[user_id]['email'] = message_text
            bot.sendMessage(chat_id, "Qual é o seu número de telefone?")
            user_states[user_id]['state'] = 'phone'

        elif user_state == 'phone':
            user_states[user_id]['phone'] = message_text
            user_name = user_states[user_id]['name']
            user_email = user_states[user_id]['email']
            user_phone = user_states[user_id]['phone']

            response = (f"Obrigado, {user_name}! Aqui estão os seus dados:\n"
                        f"Nome: {user_name}\n"
                        f"E-mail: {user_email}\n"
                        f"Telefone: {user_phone}\n\n"
                        f"Agora, clique no link abaixo para realizar o pagamento: {url}")

            bot.sendMessage(chat_id, response)
            user_states[user_id]['state'] = 'finished'

# Inicia o loop infinito para manter o chatbot em execução
bot = telepot.Bot(token)

print('Bot iniciado, esperando mensagens...')

# Inicia o loop de espera por mensagens
bot.message_loop(handle)

# Mantém o bot em execução
while True:
    time.sleep(10)


# Faz pergunta sobre nome, email e telefone do usuário e envia na mensagem personalizada junto com o link de pagamento.