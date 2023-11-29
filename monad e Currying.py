import funcoes
import mysql.connector

# Conecte-se ao banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#euamoDeus2",
    database="av3"
)



funcoes.verificar_user(db,"joao")
funcoes.saldo(db,"102000")
