import mysql.connector
import funcoes
# Função para conectar ao banco de dados
def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="#euamoDeus2",
        database="Banco_av3"
    )
db = conectar_banco()

funcoes.corrige_nascimento(db,"1234")


