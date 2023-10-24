#Após voce executar o primeiro código o "mysql connect" faça adições,alterações e remoção tudo por aqui!


import mysql.connector

# Conecte-se ao banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="lucas2003",
    database="av3_func"
)

cursor = db.cursor()


# Função para adicionar uma pessoa
def adicionar_pessoa(nome, data_nascimento):
    query = "INSERT INTO pessoas (nome, data_nascimento) VALUES (%s, %s)"
    values = (nome, data_nascimento)
    cursor.execute(query, values)
    db.commit()

# Função para visualizar todas as pessoas
def visualizar_pessoas():
    cursor.execute("SELECT * FROM pessoas")
    result = cursor.fetchall()
    for pessoa in result:
        print(pessoa)

# Função para alterar a data de nascimento de uma pessoa pelo nome
def alterar_data_nascimento(nome, nova_data_nascimento):
    query = "UPDATE pessoas SET data_nascimento = %s WHERE nome = %s"
    values = (nova_data_nascimento, nome)
    cursor.execute(query, values)
    db.commit()

# Função para apagar uma pessoa pelo nome
def apagar_pessoa(nome):
    query = "DELETE FROM pessoas WHERE nome = %s"
    values = (nome,)
    cursor.execute(query, values)
    db.commit()


visualizar_pessoas()