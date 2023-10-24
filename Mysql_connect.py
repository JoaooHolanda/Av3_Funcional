import mysql.connector

# Conecte-se ao banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="lucas2003",
    database="av3_func"
)

cursor = db.cursor()

# Crie a tabela
cursor.execute("CREATE TABLE IF NOT EXISTS pessoas (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), data_nascimento DATE)")

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



# Exemplos de adição
adicionar_pessoa("João", "1990-01-15")



visualizar_pessoas()

# Feche o cursor e a conexão
cursor.close()
db.close()
