from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import secrets  # Usaremos a biblioteca "secrets" para gerar tokens seguros
import datetime
import funcoes

app = Flask(__name__)

# Função para conectar ao banco de dados
def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="#euamoDeus2",
        database="av3_func"
    )
db = conectar_banco()
funcoes.criar_tabela_users(db)


@app.route('/')
def login():
    return render_template('login-form-18/index.html')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    username = request.form['username']
    senha = request.form['senha']

    
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


@app.route('/criaruser')
def cadastro():
    return render_template("login-form-18/Cadastro.html")    

@app.route("/cadastro",methods=['POST'])
def cadastrar_user():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']
        NomeCom = request.form['nome']
        dtnasci = request.form['dt_nasci']

        funcoes.adicionar_pessoa(db,username,senha,dtnasci,NomeCom)
    else:
        return ("Nao foi")

    return render_template('login-form-18/index.html')
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        
        return redirect(url_for('reset_password', username=username))

    return render_template('login-form-18/forgot_password.html')

@app.route('/reset_password/<username>', methods=['GET', 'POST'])
def reset_password(username):
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if new_password == confirm_password:
            funcoes.alterar_Senha(db,username,new_password)
           
            return "Senha redefinida com sucesso."
        else:
            return "As senhas não coincidem."

    return render_template('login-form-18/reset_password.html')

if __name__ == '__main__':
    app.run(debug=True)
