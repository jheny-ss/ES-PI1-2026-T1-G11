import mysql.connector

# Conexão com o banco
conexao = mysql.connector.connect(
    host='localhost',
    user='seu_usuario',
    password='sua_senha',
    database='nome_do_banco'
)

cursor = conexao.cursor()

# ---------- POST: Inserir um novo usuário ----------
def inserir_usuario(nome, email):
    sql = "INSERT INTO usuarios (nome, email) VALUES (%s, %s)"
    valores = (nome, email)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Usuário inserido com ID:", cursor.lastrowid)

# ---------- GET: Buscar todos os usuários ----------
def listar_usuarios():
    cursor.execute("SELECT id, nome, email FROM usuarios")
    for (id, nome, email) in cursor.fetchall():
        print(f"ID: {id}, Nome: {nome}, Email: {email}")

# Exemplo de uso
inserir_usuario("Joice", "joice@email.com")
listar_usuarios()