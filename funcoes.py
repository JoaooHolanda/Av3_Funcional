import mysql.connector

# Função para verificar se um usuário existe pelo nome
# Função para verificar se um usuário com um nome e data de nascimento específicos existe
def verificar_usuario(db, nome_comp, data_nascimento):
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM users WHERE NomeCompleto = %s AND DataNascimento = %s"
    cursor.execute(query, (nome_comp, data_nascimento))
    count = cursor.fetchone()[0]
    cursor.close()
    
    if count > 0:
        return True  # Usuário encontrado
    else:
        return False  # Usuário não encontrado

# Função para adicionar uma pessoa
def adicionar_pessoa(db,Username,Senha,Datanasci,nomecompleto):
    #nesse codigo ele verifica se 
    if( not verificar_usuario(db,nomecompleto,Datanasci)):
        cursor = db.cursor()
        query = "INSERT INTO users (Username,Senha,DataNascimento,NomeCompleto) VALUES (%s,%s,%s,%s)"
        values = (Username,Senha,Datanasci,nomecompleto)
        cursor.execute(query, values)
        db.commit()
        cursor.close()
    else:
        print("Usuário já existe")

# Função para visualizar todas as pessoas
def visualizar_pessoas(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM pessoas")
    result = cursor.fetchall()
    for pessoa in result:
        print(pessoa)
    cursor.close()



# Função para alterar a data de nascimento de uma pessoa pelo nome
def alterar_Senha(db, username,novasenha):
    
    cursor = db.cursor()
    query = "UPDATE users SET Senha = %s WHERE username = %s"
    values = (novasenha, username)
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

# Função para criar a tabela "users"
def criar_tabela_users(db):
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        Username VARCHAR(255) PRIMARY KEY,
        Senha VARCHAR(255),
        NomeCompleto VARCHAR(255),
        DataNascimento DATE
        
    )
    """)
    db.commit()
    cursor.close()