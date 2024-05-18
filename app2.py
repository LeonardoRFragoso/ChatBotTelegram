import telepot
import time

# Insira o token do seu bot aqui
token = "6933320373:AAHVNQ_4NQ0VU1rrA9_06ydNR-53cCwUPeI"

# URL do serviço
url = "https://pay.kiwify.com.br/MXMKc1H"

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type == 'text':
        message_text = msg['text']
        
        if message_text.startswith('/start'):
            user_name = msg['from']['first_name']
            response = f"Olá {user_name}! Clique no link abaixo para realizar o pagamento: {url}"
            bot.sendMessage(chat_id, response)

# Inicia o loop infinito para manter o chatbot em execução
bot = telepot.Bot(token)

print('Bot iniciado, esperando mensagens...')

# Inicia o loop de espera por mensagens
bot.message_loop(handle)

# Mantém o bot em execução
while True:
    time.sleep(10)


# Envia o link de pagamento personalizado com o nome do usuário do telegram na mensagem