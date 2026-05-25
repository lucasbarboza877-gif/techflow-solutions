import sqlite3
import os

# Caminho do banco de dados
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'taskflow.db')

def get_conexao():
    """Retorna uma conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # permite acessar colunas pelo nome
    return conn

def inicializar_banco():
    """Cria as tabelas do banco se elas ainda não existirem."""
    conn = get_conexao()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT DEFAULT 'a_fazer',
            prioridade TEXT DEFAULT 'media',
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso!")

 
