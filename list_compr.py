import mysql.connector

# Conectar-se ao banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#euamoDeus2",
    database="sprint3"
)

# Função auxiliar para obter dados do banco de dados
def obter_dados(username):
    cursor = db.cursor(buffered=True)
    cursor.execute(f"SELECT username, senha FROM users WHERE username = '{username}'")
    return cursor.fetchone()

# Função lambda que utiliza list comprehension para obter dados do banco de dados
obter_dados_usuario = lambda username: [({'username': resultado[0], 'senha': resultado[1]} if resultado else None) for resultado in [obter_dados(username)]][0]

# Exemplo de uso
dados_usuario = obter_dados_usuario('admin1')

if dados_usuario:
    print(f"Dados do usuário: {dados_usuario}")
else:
    print("Usuário não encontrado.")
