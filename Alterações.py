import mysql.connector
import funcoes

# Conecte-se ao banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#euamoDeus2",
    database="av3_func"
)

# Exemplos de uso das funções do módulo funcoes
# funcoes.adicionar_pessoa(db,"Maria","2002/04/25")
funcoes.apagar_pessoa(db,"joel","2003/04/02")
funcoes.visualizar_pessoas(db)

# Feche a conexão quando terminar
db.close()
