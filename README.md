# PyScript.Tech Lead Generation Bot

Este é um bot do Telegram desenvolvido para gerar leads para a PyScript.Tech. Ele coleta informações de usuários interessados em serviços como Desenvolvimento Web, Criação de Bots e Automação com Python, e envia essas informações por e-mail e notifica no Telegram.

## Funcionalidades

- Coleta de nome, sobrenome, interesse e descrição da necessidade do usuário.
- Registra os leads em um banco de dados SQLite.
- Atualiza uma planilha Excel com os dados dos leads.
- Envia um e-mail com a planilha atualizada.
- Notifica um ID do Telegram com os detalhes do novo lead.

## Pré-requisitos

- Python 3.x
- Bibliotecas Python: telepot, openpyxl, smtplib, sqlite3

## Como usar

1. Clone este repositório.
2. Instale as dependências necessárias:
    ```sh
    pip install telepot openpyxl
    ```
3. Substitua o token do bot e outras informações necessárias no código.
4. Execute o bot:
    ```sh
    python app.py
    ```

## Hospedagem

Este bot está hospedado na Amazon Web Services (AWS) utilizando uma instância EC2. Para mais informações sobre como configurar uma instância EC2, consulte a [documentação da AWS](https://aws.amazon.com/documentation/ec2/).

## Funções do Bot

### registrar_lead
Insere um registro de lead no banco de dados SQLite e executa funções para enviar mensagem pessoal, atualizar planilha e enviar email.

### enviar_mensagem_pessoal
Envia uma mensagem com detalhes do lead para um ID específico no Telegram.

### atualizar_planilha
Atualiza ou cria uma planilha Excel com os dados do lead.

### enviar_email
Envia a planilha atualizada por e-mail para uma lista de destinatários.

### handle
Manipula as mensagens recebidas pelo bot e gerencia os estados da conversa com o usuário.

## Inicialização

O bot inicia um loop infinito para manter-se em execução e espera por mensagens dos usuários.

Para mais detalhes sobre o código e seu funcionamento, consulte o arquivo `app.py`.
