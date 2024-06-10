# Telepot Payment Bot

Este é um bot Telegram que facilita o processo de pagamento para os usuários. O bot interage com os usuários, coleta informações de pagamento e registra os pagamentos em um banco de dados SQLite.

Funcionalidades:

Solicita o nome e sobrenome do usuário.
Fornece um link para realizar o pagamento.
Registra se o pagamento foi confirmado ou não.

Requisitos:
Python 3
Biblioteca Telepot
Banco de dados SQLite

Configuração

Instale as dependências necessárias executando o seguinte comando:
pip install telepot

Insira o token do seu bot no script. O token pode ser obtido criando um novo bot com o BotFather no Telegram.

Defina a URL do serviço para a qual os usuários serão redirecionados para efetuar o pagamento.

Certifique-se de ter permissão para criar e escrever em um arquivo de banco de dados SQLite. O script usará um arquivo chamado pagamentos.db para armazenar os registros de pagamento.

Uso:

Execute o script Python.

python3 app.py

Inicie uma conversa com o bot no Telegram. Você pode usar o comando /start para iniciar a interação.

Siga as instruções do bot para fornecer seu nome, sobrenome e confirmar o pagamento.

O bot registrará o pagamento no banco de dados e fornecerá feedback ao usuário.

Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests para melhorar este bot.

Autor
Este bot foi desenvolvido por Leonardo Fragoso .
