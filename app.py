import telepot
import time

# Insira o token do seu bot aqui
token = "6933320373:AAHVNQ_4NQ0VU1rrA9_06ydNR-53cCwUPeI"
# URL do serviço
url = "https://pay.kiwify.com.br/MXMKc1H"

def handle(msg):
    chat_id = msg['chat']['id']
    message_text = msg['text']

    if message_text.startswith('/start'):
        response = f"Olá! Acesse o link para realizar o pagamento: {url}"
        bot.sendMessage(chat_id, response)

# Inicia o bot
bot = telepot.Bot(token)

# Desativa o webhook
bot.deleteWebhook()

# Inicia o loop de espera por mensagens
bot.message_loop(handle)

print("Bot iniciado, esperando mensagens...")

# Mantém o script em execução
while True:
    time.sleep(10)  # Espera 10 segundos antes de verificar novamente as mensagens



# envia o link de pagamento direto