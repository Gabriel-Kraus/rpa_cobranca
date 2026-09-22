import sqlite3

def init_db():
    conn = sqlite3.connect('cobranca.db')
    cursor = conn.cursor()

    # Tabela de Clientes (Parte 1 do trabalho)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL,
            endereco TEXT NOT NULL
        )
    ''')

    # Tabela de Faturas e Cobranças
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            valor REAL NOT NULL,
            vencimento TEXT NOT NULL,
            status TEXT DEFAULT 'Pendente',
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Banco de dados SQLite inicializado com sucesso!")

if __name__ == '__main__':
    init_db()