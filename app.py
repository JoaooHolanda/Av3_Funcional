from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Função para conectar ao banco de dados
def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="#euamoDeus2",
        database="av3_func"
    )

@app.route('/')
def login():
    return render_template('login-form-18/index.html')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    username = request.form['username']
    senha = request.form['senha']

    db = conectar_banco()
    cursor = db.cursor()

    query = "SELECT Username, Senha FROM users WHERE Username = %s AND Senha = %s"
    cursor.execute(query, (username, senha))
    result = cursor.fetchone()
    
    cursor.close()
    db.close()

    if result:
        return "Login bem-sucedido!"
    else:
        return "Login falhou. Verifique suas credenciais."

if __name__ == '__main__':
    app.run(debug=True)
