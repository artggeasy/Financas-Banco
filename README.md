# 💰 Sistema de Controle Financeiro Pessoal

Este é um sistema de **controle financeiro pessoal** desenvolvido com **Python + Streamlit** e utilizando **SQLite** como banco de dados.  
O projeto permite gerenciar receitas, despesas, categorias e visualizar um resumo financeiro com gráficos.

---

## 🚀 Funcionalidades

### 🔐 Autenticação
- Cadastro de usuários
- Login seguro (com senha criptografada em SHA-256)
- Controle de sessão (mantém o usuário logado)

### 🏠 Página Inicial (Dashboard)
- Resumo financeiro com:
  - Total de receitas
  - Total de despesas
  - Saldo consolidado
- Gráfico simples de receitas vs despesas

### 📂 Categorias
- Criar categorias de **Receita** ou **Despesa**
- Listar categorias registradas

### 💸 Transações
- Registrar receitas e despesas
- Selecionar categoria
- Definir valor, descrição e data
- Histórico completo de transações

### 🔧 Banco de Dados SQLite
- Tabelas:
  - `usuarios`
  - `categorias`
  - `transacoes`
- Relacionamentos via chave estrangeira
- Atualização e remoção em cascata

---

## 🛠 Tecnologias utilizadas

- **Python 3.x**
- **Streamlit**
- **SQLite3**
- **Pandas**
- **Hashlib**
- **Datetime**

---

## 📦 Instalação
Clone este repositório:
```bash
git clone https://github.com/artggeasy/Financas-Banco
.git
cd seu-repo

Crie um ambiente virtual (opcional, mas recomendado):
python -m venv venv

Ative o ambiente:
Windows:venv\Scripts\activate

Instale as dependências:
pip install -r requirements.txt

▶️ Execução
Para iniciar o sistema, execute:
streamlit run app.py
O navegador abrirá automaticamente com a interface do sistema.

🗄 Estrutura do Projeto
📁 projeto-financeiro
├── app.py                # Código principal (Streamlit)
├── criar_bd.py           # Script para criação do banco de dados
├── financeiro.db         # Banco de dados (gerado automatic. após rodar)
├── requirements.txt      # Dependências
└── README.md             # Documentação do projeto
🗃 Banco de Dados
O banco é criado automaticamente via script:

Tabelas:
👤 usuarios
Campo	Tipo	Obs
id_usuario	INTEGER	PK, Auto
nome	TEXT	obrigatório
email	TEXT	único
senha	TEXT	criptografada

🏷 categorias
Campo	Tipo	Obs
id_categoria	INTEGER	PK
id_usuario	INTEGER	FK → usuarios
nome	TEXT	obrigatório
tipo	TEXT	Receita / Despesa

💵 transacoes
Campo	Tipo	Obs
id_transacao	INTEGER	PK
id_usuario	INTEGER	FK
id_categoria	INTEGER	FK
descricao	TEXT	
valor	REAL	
tipo	TEXT (Receita/Despesa)	
data	DATE	

🧑‍💻 Autor
Arthur da Silva Araújo

Projeto desenvolvido para aprendizado de: Python
Streamlit, Banco de dados SQLite, Lógica financeira

⭐ Contribuições
Sugestões e melhorias são sempre bem-vindas!
Sinta-se à vontade para abrir issues ou enviar pull requests.

📄 Licença
Este projeto está sob a licença MIT.
Você pode usar, modificar e distribuir livremente.
