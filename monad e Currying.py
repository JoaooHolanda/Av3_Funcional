import funcoes
import mysql.connector

# Conecte-se ao banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#euamoDeus2",
    database="sprint3"
)



funcoes.verificar_user(db,None)
funcoes.saldo(db,"600000000")
