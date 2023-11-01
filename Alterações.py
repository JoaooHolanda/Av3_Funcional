import mysql.connector
import funcoes

# Conecte-se ao banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#euamoDeus2",
    database="sprint1"
)

crs = db.cursor()

execsqlcmd = lambda cmd, crs: crs.execute (cmd)

apagar_usuario = lambda teste, crs: execsqlcmd(f"DELETE FROM pessoas WHERE nome = '{teste}';", crs)




funcoes.criar_tabela_pessoas(db)
# Exemplos de uso das funções do módulo funcoes
#funcoes.adicionar_pessoa(db,"pedro","2002/04/25")
#apagar_usuario("pedro",crs)
#funcoes.visualizar_pessoas(db)
#funcoes.alterar_data_nascimento(db,"PEDRO","2011/04/25")

# Feche a conexão quando terminar

db.commit()
crs.close()
