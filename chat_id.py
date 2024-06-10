import telepot
import time

# Insira o token do seu bot aqui
token = "6933320373:AAHVNQ_4NQ0VU1rrA9_06ydNR-53cCwUPeI"

# Função para manipular as mensagens recebidas
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(f"chat_id: {chat_id}")

# Inicia o loop infinito para manter o chatbot em execução
bot = telepot.Bot(token)

print('Bot iniciado, esperando mensagens...')

# Inicia o loop de espera por mensagens
bot.message_loop(handle)

# Mantém o bot em execução
while True:
    time.sleep(10)
