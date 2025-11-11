import sqlite3

conn = sqlite3.connect("financeiro.db")
cursor = conn.cursor()

#tabela de usuários
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
);
""")

#tabela de categorias
cursor.execute("""
CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    nome TEXT NOT NULL,
    tipo TEXT CHECK(tipo IN ('Receita', 'Despesa')) NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        ON DELETE CASCADE ON UPDATE CASCADE
);
""")

#tabela de transações
cursor.execute("""
CREATE TABLE IF NOT EXISTS transacoes (
    id_transacao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_categoria INTEGER NOT NULL,
    descricao TEXT,
    valor REAL NOT NULL,
    tipo TEXT CHECK(tipo IN ('Receita', 'Despesa')) NOT NULL,
    data DATE NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
        ON DELETE SET NULL ON UPDATE CASCADE
);
""")

conn.commit()
conn.close()
print("Banco de dados criado com sucesso!")