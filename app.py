import streamlit as st
import sqlite3
import hashlib
from datetime import date
import pandas as pd


#funções de banco de dados
def conectar():
    return sqlite3.connect("financeiro.db")

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

#usuários
def criar_usuario(nome, email, senha):
    conn=conectar()
    cur=conn.cursor()
    try:
        cur.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                    (nome, email, hash_senha(senha)))
        conn.commit()
        st.success("✅ Usuário cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        st.error("❌ E-mail já cadastrado.")
    conn.close()

def login(email, senha):
    conn=conectar()
    cur=conn.cursor()
    cur.execute("SELECT id_usuario, nome FROM usuarios WHERE email=? AND senha=?",
                (email, hash_senha(senha)))
    user=cur.fetchone()
    conn.close()
    return user

#categorias
def listar_categorias(id_usuario, tipo=None):
    conn=conectar()
    cur=conn.cursor()
    if tipo:
        cur.execute("SELECT id_categoria, nome FROM categorias WHERE id_usuario=? AND tipo=?",
                    (id_usuario, tipo))
    else:
        cur.execute("SELECT id_categoria, nome, tipo FROM categorias WHERE id_usuario=?",
                    (id_usuario,))
    categorias=cur.fetchall()
    conn.close()
    return categorias

def criar_categoria(id_usuario, nome, tipo):
    conn=conectar()
    cur=conn.cursor()
    cur.execute("INSERT INTO categorias (id_usuario, nome, tipo) VALUES (?, ?, ?)",
                (id_usuario, nome, tipo))
    conn.commit()
    conn.close()
    st.success("✅ Categoria criada com sucesso!")

#transações
def adicionar_transacao(id_usuario, id_categoria, descricao, valor, tipo, data):
    conn=conectar()
    cur=conn.cursor()
    cur.execute("""
        INSERT INTO transacoes (id_usuario, id_categoria, descricao, valor, tipo, data)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_usuario, id_categoria, descricao, valor, tipo, data))
    conn.commit()
    conn.close()
    st.success("✅ A Transação registrada!")

def listar_transacoes(id_usuario):
    conn=conectar()
    cur=conn.cursor()
    cur.execute("""
        SELECT t.id_transacao, c.nome, t.descricao, t.valor, t.tipo, t.data
        FROM transacoes t
        JOIN categorias c ON t.id_categoria = c.id_categoria
        WHERE t.id_usuario=?
        ORDER BY t.data DESC
    """, (id_usuario,))
    dados=cur.fetchall()
    conn.close()
    return dados

def resumo_financeiro(id_usuario):
    conn=conectar()
    cur=conn.cursor()

    cur.execute("""
        SELECT tipo, SUM(valor)
        FROM transacoes
        WHERE id_usuario=?
        GROUP BY tipo
    """, (id_usuario,))

    resultados=cur.fetchall()
    conn.close()

    receitas=sum(r[1] for r in resultados if r[0] == "Receita")
    despesas=sum(r[1] for r in resultados if r[0] == "Despesa")
    saldo=receitas-despesas

    return receitas, despesas, saldo

#Menu do meu Streamlit

st.set_page_config(page_title="💰 Controle Financeiro", layout="centered")
st.title("💰 Sistema de Controle Financeiro Pessoal")

# LOGIN E CADASTRO
# Se já estiver logado pula login
if "user" not in st.session_state:

    menu=["Login", "Cadastro"]
    opcao=st.sidebar.selectbox("Menu", menu)

    if opcao == "Cadastro":
        st.subheader("📋 Criar nova conta")
        nome=st.text_input("Nome")
        email=st.text_input("Email")
        senha=st.text_input("Senha", type="password")

        if st.button("Cadastrar"):
            if nome and email and senha:
                criar_usuario(nome, email, senha)
            else:
                st.warning("Preencha todos os campos.")

    elif opcao == "Login":
        st.subheader("🔐 Acessar sistema")
        email=st.text_input("Email")
        senha=st.text_input("Senha", type="password")

        if st.button("Entrar"):
            user=login(email, senha)
            if user:
                st.session_state["user"] = {"id": user[0], "nome": user[1]}
                st.rerun()
            else:
                st.error("E-mail ou senha incorretos.")

# áreas das abas dos lados ja logado
if "user" in st.session_state:
    user = st.session_state["user"]
    st.sidebar.write(f"👤 Usuário: **{user['nome']}**")

    aba = st.sidebar.radio(
        "Navegar",
        ["🏠 Início", "📂 Categorias", "💸 Transações", "🚪 Sair"]
    )

    
    #grafico e resumo financeiro

    if aba == "🏠 Início":
        st.subheader("📊 Resumo Financeiro")

        receitas, despesas, saldo = resumo_financeiro(user["id"])

        col1, col2, col3 = st.columns(3)
        col1.metric("Receitas", f"R$ {receitas:.2f}")
        col2.metric("Despesas", f"R$ {despesas:.2f}")
        col3.metric("Saldo", f"R$ {saldo:.2f}")

        # Gráfico simples
        df_graf=pd.DataFrame(
            {"Tipo": ["Receitas", "Despesas"], "Valor": [receitas, despesas]}
        ).set_index("Tipo")

        st.bar_chart(df_graf)

    #categorias
    elif aba == "📂 Categorias":
        st.subheader("🏷️ Minhas Categorias")

        categorias = listar_categorias(user["id"])
        if categorias:
            df = pd.DataFrame(categorias, columns=["ID", "Nome", "Tipo"])
            st.dataframe(df, use_container_width=True)

        nome_cat = st.text_input("Nome da categoria")
        tipo_cat = st.selectbox("Tipo", ["Receita", "Despesa"])

        if st.button("Adicionar categoria"):
            if nome_cat:
                criar_categoria(user["id"], nome_cat, tipo_cat)
                st.rerun()
            else:
                st.warning("Informe o nome da categoria.")

    #transaçõess
    elif aba == "💸 Transações":
        st.subheader("💸 Minhas Transações")

        tipo_trans = st.selectbox("Tipo", ["Receita", "Despesa"])

        categorias=listar_categorias(user["id"], tipo_trans)
        cat_nomes=[c[1] for c in categorias]

        if cat_nomes:
            cat_escolhida=st.selectbox("Categoria", cat_nomes)
            id_cat=[c[0] for c in categorias if c[1] == cat_escolhida][0]

            descricao=st.text_input("Descrição")
            valor=st.number_input("Valor", min_value=0.0, format="%.2f")
            data_trans=st.date_input("Data", value=date.today())

            if st.button("Adicionar transação"):
                adicionar_transacao(
                    user["id"], id_cat, descricao, valor, tipo_trans, data_trans
                )
                st.rerun()

            st.write(">>> 📋 Histórico de Transações")
            dados = listar_transacoes(user["id"])

            if dados:
                df = pd.DataFrame(
                    dados,
                    columns=["ID", "Categoria", "Descrição", "Valor", "Tipo", "Data"]
                )
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Nenhuma transação registrada.")

        else:
            st.warning("Crie uma categoria antes de lançar transações.")

    # ------------------------------
    # LOGOUT
    # ------------------------------
    elif aba == "🚪 Sair":
        st.session_state.pop("user")
        st.success("Logout realizado com sucesso!")
        st.rerun()
