from flask import Flask, render_template, request, redirect, url_for, flash
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
        database="Banco_av3"
    )
db = conectar_banco()
funcoes.criar_tabela_users(db)


@app.route('/')
def login():
    return render_template('login-form-18/index.html')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    db = conectar_banco()
    username = request.form['username']
    senha = request.form['senha']

    cursor = db.cursor()

    query = "SELECT Username, Senha, NomeCompleto, DataNascimento FROM users WHERE Username = %s AND Senha = %s"
    cursor.execute(query, (username, senha))
    result = cursor.fetchone()
    
    
    cursor.close()
    db.close()
    if result:
        nome = result[2]
        data_de_nascimento = result[3]

        return redirect('/profile?nome={}&data_de_nascimento={}'.format(nome, data_de_nascimento))

    else:
        # Login falhou
        # Adicione o script para mostrar um toast
        toast_script = """
        <script>
            Toastify({
                text: "Login falhou. Verifique suas credenciais.",
                duration: 5000,  // Duração do toast em milissegundos (opcional)
                gravity: "top",  // Posição do toast (opcional)
                backgroundColor: "red"  // Cor de fundo do toast (opcional)
            }).showToast();
        </script>
        """
        return render_template('login-form-18/index.html', toast_script=toast_script)
    

#mostrando o perfil
@app.route('/profile')
def profile():
    nome = request.args.get('nome')
    data_de_nascimento = request.args.get('data_de_nascimento')
    toast_script = """
        <script>
            Toastify({
                text: "Login feito com sucesso! Bem vindo",
                duration: 5000,  // Duração do toast em milissegundos (opcional)
                gravity: "top",  // Posição do toast (opcional)
                backgroundColor: "green"  // Cor de fundo do toast (opcional)
            }).showToast();
        </script>
        """
    return render_template("login-form-18/Profile.html", nome=nome, data_de_nascimento=data_de_nascimento,toast_script=toast_script)

#criando o user
@app.route('/criaruser')
def cadastro():
    return render_template("login-form-18/Cadastro.html")    


#Cadastrando ususarios no banco
@app.route("/cadastro",methods=['POST'])
def cadastrar_user():
    db = conectar_banco()
    
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']
        NomeCom = request.form['nome']
        dtnasci = request.form['dt_nasci']
        saldo = float(request.form['saldo'])
        cpf = request.form['cpf']

        funcoes.adicionar_pessoa(db,username,senha,dtnasci,NomeCom,saldo,cpf)
    
    toast_script = """
        <script>
            Toastify({
                text: "Usuário Criado com Sucesso",
                duration: 5000,  // Duração do toast em milissegundos (opcional)
                gravity: "top",  // Posição do toast (opcional)
                backgroundColor: "green"  // Cor de fundo do toast (opcional)
            }).showToast();
        </script>
        """
    return render_template('login-form-18/index.html',toast_script=toast_script)


#tela de esqeuci a senha
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']

        # Realize uma consulta ao banco de dados para verificar se o usuário existe
        db = conectar_banco()
        cursor = db.cursor()

        query = "SELECT Username FROM users WHERE Username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        cursor.close()
        db.close()

        if result:
            # Se o usuário existe, redirecione para a página de redefinição de senha
            return redirect(url_for('reset_password', username=username))
        else:
            # usuario nao foi encontrado
            # Adicione o script para mostrar um toast
            toast_script = """
            <script>
                Toastify({
                    text: "Usario não encontrado!",
                    duration: 5000,  // Duração do toast em milissegundos (opcional)
                    gravity: "top",  // Posição do toast (opcional)
                    backgroundColor: "yellow"  // Cor de fundo do toast (opcional)
                }).showToast();
            </script>
            """
            return render_template('login-form-18/forgot_password.html', toast_script=toast_script)

    return render_template('login-form-18/forgot_password.html')



#trocando a senha no banco
@app.route('/reset_password/<username>', methods=['GET', 'POST'])
def reset_password(username):
    # Certifique-se de que a conexão com o banco de dados seja criada dentro da função
    db = conectar_banco()
    cursor = db.cursor()

    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if new_password == confirm_password:
            funcoes.alterar_Senha(db, username, new_password)
            cursor.close()  # Feche o cursor
            db.close()  # Feche a conexão

            toast_script = """
                <script>
                    Toastify({
                        text: "Senha alterada com sucesso",
                        duration: 5000,  // Duração do toast em milissegundos (opcional)
                        gravity: "top",  // Posição do toast (opcional)
                        backgroundColor: "green"  // Cor de fundo do toast (opcional)
                    }).showToast();
                </script>
                 """
            return render_template('login-form-18/index.html',toast_script=toast_script)
            
        else:
            cursor.close()  # Feche o cursor
            db.close()  # Feche a conexão
        #senhas nao coincidem 
        # Adicione o script para mostrar um toast
        toast_script = """
        <script>
            Toastify({
                text: "Senhas não coincidem",
                duration: 5000,  // Duração do toast em milissegundos (opcional)
                gravity: "top",  // Posição do toast (opcional)
                backgroundColor: "red"  // Cor de fundo do toast (opcional)
            }).showToast();
        </script>
        """
        return render_template('login-form-18/reset_password.html', toast_script=toast_script)

    # Certifique-se de fechar a conexão e o cursor mesmo se não houver um envio POST
    cursor.close()
    db.close()

    return render_template('login-form-18/reset_password.html')



if __name__ == '__main__':
    app.run(debug=True)
