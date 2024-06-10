import sqlite3

def criar_ou_atualizar_tabela():
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()

    # Criar a tabela se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            user_name TEXT NOT NULL,
            user_last_name TEXT,
            user_username TEXT,
            telefone TEXT,
            email TEXT,
            interesse TEXT NOT NULL,
            descricao TEXT
        )
    ''')

    # Verificar se as colunas necessárias existem e adicioná-las se estiverem faltando
    cursor.execute('PRAGMA table_info(leads)')
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'telefone' not in columns:
        cursor.execute('ALTER TABLE leads ADD COLUMN telefone TEXT')
    
    if 'email' not in columns:
        cursor.execute('ALTER TABLE leads ADD COLUMN email TEXT')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_ou_atualizar_tabela()
    print("Tabela 'leads' criada ou atualizada com sucesso.")
