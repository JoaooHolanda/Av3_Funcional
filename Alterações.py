import mysql.connector


# Conecte-se ao banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#euamoDeus2",
    database="sprint2"
)

crs = db.cursor()

execsqlcmd = lambda cmd, crs: crs.execute (cmd)

apagar_usuario = lambda teste, crs: execsqlcmd(f"DELETE FROM users WHERE Username = '{teste}';", crs)



apagar_usuario("pedro",crs)


# Feche a conexão quando terminar
db.commit()
crs.close()
