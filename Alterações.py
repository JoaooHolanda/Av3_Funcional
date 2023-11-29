import mysql.connector


# Conecte-se ao banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#euamoDeus2",
    database="av3"
)

crs = db.cursor()

execsqlcmd = lambda cmd, crs: crs.execute (cmd)

apagar_usuario = lambda teste, crs,func: func(f"DELETE FROM users WHERE Username = '{teste}';", crs)


apagar_usuario("admin1",crs,execsqlcmd)


# Feche a conexão quando terminar
db.commit()
crs.close()
