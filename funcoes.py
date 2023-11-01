import mysql.connector


# Função para criar a tabela "users"
def criar_tabela_pessoas(db):
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pessoas (
        nome VARCHAR(255) PRIMARY KEY,     
        data_nascimento DATE  
    )
    """)
    db.commit()
    cursor.close()

# Função para verificar se um usuário existe pelo nome
# Função para verificar se um usuário com um nome e data de nascimento específicos existe
def verificar_usuario(db, nome, data_nascimento):
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM pessoas WHERE nome = %s AND data_nascimento = %s"
    cursor.execute(query, (nome, data_nascimento))
    count = cursor.fetchone()[0]
    cursor.close()
    
    if count > 0:
        return True  # Usuário encontrado
    else:
        return False  # Usuário não encontrado

# # Função para adicionar uma pessoa
# def adicionar_pessoa(db, nome, data_nascimento):
#     #nesse codigo ele verifica se 
#     if( not verificar_usuario(db,nome,data_nascimento)):
#         cursor = db.cursor()
#         query = "INSERT INTO pessoas (nome, data_nascimento) VALUES (%s, %s)"
#         values = (nome, data_nascimento)
#         cursor.execute(query, values)
#         db.commit()
#         cursor.close()
#     else:
#         print("Usuário já existe")

adicionar_pessoa = lambda db, nome, data_nascimento: (db.cursor().execute("INSERT INTO pessoas (nome, data_nascimento) VALUES (%s, %s)", (nome, data_nascimento)) and db.commit()) or db.cursor().close()



# Função para visualizar todas as pessoas
def visualizar_pessoas(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM pessoas")
    result = cursor.fetchall()
    for pessoa in result:
        print(pessoa)
    cursor.close()



# Função para alterar a data de nascimento de uma pessoa pelo nome
def alterar_data_nascimento(db, nome, nova_data_nascimento):
    cursor = db.cursor()
    query = "UPDATE pessoas SET data_nascimento = %s WHERE nome = %s"
    values = (nova_data_nascimento, nome)
    cursor.execute(query, values)
    db.commit()
    cursor.close()

# # Função para apagar uma pessoa pelo nome
# def apagar_pessoa(db, nome,data_nascimento):
#     if(verificar_usuario(db,nome,data_nascimento)):
#         cursor = db.cursor()
#         query = "DELETE FROM pessoas WHERE nome = %s"
#         values = (nome,)
#         cursor.execute(query, values)
#         db.commit()
#         cursor.close()
#     else:
#         print("Usuário não existe para ser apagado")

# apagar_pessoa = lambda db, nome, data_nascimento: (
#     (lambda cursor, query, values: cursor.execute(query, values) and db.commit())(db.cursor(), "DELETE FROM pessoas WHERE nome = %s", (nome,))
# ) if (lambda cursor, nome, data_nascimento: cursor.execute("SELECT COUNT(*) FROM pessoas WHERE nome = %s AND data_nascimento = %s", (nome, data_nascimento)) and cursor.fetchone()[0] > 0)(db.cursor(), nome, data_nascimento) else print("Usuário não existe para ser apagado")

