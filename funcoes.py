import mysql.connector
import datetime



# Função para verificar se um usuário existe pelo nome
# Função para verificar se um usuário com um nome e data de nascimento específicos existe
def verificar_cpf(db, cpf):
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM users WHERE CPF = %s "
    cursor.execute(query, (cpf,))
    count = cursor.fetchone()[0]
    cursor.close()
    
    if count > 0:
        return True  # Usuário encontrado
    else:
        return False  # Usuário não encontrado

# Função para criar um novo hash de senha para o usuário ao se cadastrar ou alterar a senha
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return salt, hashed_password


def verificar_user(db, user):
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM users WHERE Username = %s "
    cursor.execute(query, (user,))
    count = cursor.fetchone()[0]
    cursor.close()
    
    if count > 0:
        return True  # Usuário encontrado
    else:
        return False  # Usuário não encontrado
import bcrypt

# Função para adicionar uma pessoa
def adicionar_pessoa(db, Username, Senha, Datanasci, nomecompleto, saldo, cpf):
    # Verifique se o CPF e o nome de usuário já existem
    if not verificar_cpf(db, cpf) and not verificar_user(db, Username):
        cursor = db.cursor()
        
        # Crie um hash de senha e obtenha o "salt" e o hash
        salt, hashed_password = hash_password(Senha)
        
        query = "INSERT INTO users (Username, Salt, Senha, DataNascimento, NomeCompleto, Saldo, CPF) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (Username, salt, hashed_password, Datanasci, nomecompleto, saldo, cpf)
        cursor.execute(query, values)


        query1 = "INSERT INTO acess(Username) VALUES (%s)"
        values1 = (Username,)
        cursor.execute(query1,values1)
        
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



# Função para alterar a senha de uma pessoa pelo nome
def alterar_Senha(db, username,novasenha):
    
    cursor = db.cursor()
    
    # Crie um hash de senha e obtenha o "salt" e o hash
    salt, hashed_password = hash_password(novasenha)

    query = "UPDATE users SET Senha = %s WHERE username = %s"
    values = (hashed_password, username)
    cursor.execute(query, values)

    query1 = "UPDATE users SET salt = %s WHERE username = %s"
    value1 = (salt,username)
    cursor.execute(query1,value1)
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
        salt VARCHAR(255),
        Senha VARCHAR(255),
        NomeCompleto VARCHAR(255),
        DataNascimento DATE,
        Saldo FLOAT,
        CPF VARCHAR(14)
        
    )
    """)
    db.commit()
    cursor.close()

def criar_tabela_acess(db):
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS acess (
        Username VARCHAR(255) PRIMARY KEY,
        Ultimo_Acesso DATETIME
    )
    """)
    db.commit()
    cursor.close()



def ultimo_acess(db, username):
    cursor = db.cursor()
    query = "UPDATE acess SET Ultimo_Acesso = NOW() WHERE Username = %s"
    
    values = (username,)
    cursor.execute(query, values)
    db.commit()

def saldo(db,cpf):
    cursor = db.cursor()
    query = "SELECT Saldo FROM users WHERE CPF = %s"
    value = (cpf,)
    cursor.execute(query, value)
    valor = cursor.fetchall()
    saldo = float(valor[0][0])
    
    return saldo



def saque(db,cpf,valor_de_saque):
    valor_de_saque = float(valor_de_saque)
    cursor = db.cursor()
    query = "SELECT Saldo FROM users WHERE CPF = %s"
    value = (cpf,)
    cursor.execute(query, value)
    valor = cursor.fetchall()
    valor = float(valor[0][0])
    saldo = valor - valor_de_saque
    saldo = str(saldo)
    new_query = "UPDATE users SET Saldo = %s WHERE CPF = %s"
    values = (saldo,cpf)
    cursor.execute(new_query,values)
    db.commit()
    cursor.close()


def deposito(db,cpf,valor_de_deposito):  
    valor_de_deposito = float(valor_de_deposito)
    cursor = db.cursor()
    query = "SELECT Saldo FROM users WHERE CPF = %s"
    value = (cpf,)
    cursor.execute(query, value)
    valor = cursor.fetchall()
    valor = float(valor[0][0])
    saldo = valor + valor_de_deposito
    saldo = str(saldo)
    new_query = "UPDATE users SET Saldo = %s WHERE CPF = %s"
    values = (saldo,cpf)
    cursor.execute(new_query,values)
    db.commit()
    cursor.close()

def corrige_nascimento(db,cpf):
    cursor = db.cursor()
    query = "SELECT DataNascimento from users where CPF = %s"
    value = (cpf,)
    cursor.execute(query,value)
    valor = cursor.fetchall()
    valor = str(valor[0][0])
    print(valor)