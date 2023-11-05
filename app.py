import bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash,session
import mysql.connector
import secrets  # Usaremos a biblioteca "secrets" para gerar tokens seguros
import datetime
from datetime import datetime
import funcoes
import hashlib

app = Flask(__name__)
app.secret_key = '#euamoDeus2'
# Função para conectar ao banco de dados
def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="#euamoDeus2",
        database="sprint3"
    )
db = conectar_banco()

funcoes.criar_tabela_users(db)
funcoes.criar_tabela_acess(db)


@app.route('/')
def login():
    return render_template('login-form-18/index.html')


# Função para criar um novo hash de senha para o usuário ao se cadastrar ou alterar a senha
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return salt, hashed_password

# Função para verificar a senha durante o login
def check_password(input_password, salt, hashed_password):
    new_hashed_password = bcrypt.hashpw(input_password.encode('utf-8'), salt)
    return new_hashed_password == hashed_password

@app.route('/autenticar', methods=['POST'])
def autenticar():
    db = conectar_banco()
    username = request.form['username']
    senha = request.form['senha']

    cursor = db.cursor()

    query = "SELECT Username, Senha, NomeCompleto, DataNascimento, CPF, Salt FROM users WHERE Username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    
    if result:
        stored_password = result[1].encode('utf-8')  # Senha armazenada no banco, convertida para bytes
        salt = result[5].encode('utf-8')  # O "salt" armazenado no banco, convertido para bytes

        if check_password(senha, salt, stored_password):  # Não converta a senha de entrada para bytes
            username = result[0]
            nome = result[2]
            data_de_nascimento = result[3]
            cpf = result[4]
            funcoes.ultimo_acess(db,username)

            # Armazene os dados na sessão
            session['nome'] = nome
            session['data_de_nascimento'] = data_de_nascimento
            session['cpf'] = cpf

            cursor.close()
            db.close()

            return redirect('/profile')
    # Login falhou
    # Adicione o script para mostrar um toast
    toast_script = """
    <script>
        Toastify({
            text: "Login falhou. Verifique suas credenciais.",
            duration: 5000,
            gravity: "top",
            backgroundColor: "red"
        }).showToast();
    </script>
    """
    return render_template('login-form-18/index.html', toast_script=toast_script)


    

# Página de perfil
@app.route('/profile')
def profile():
    # Recupere os dados da sessão
    nome = session.get('nome', None)
    data_de_nascimento = session.get('data_de_nascimento', None)
    cpf = session.get('cpf', None)

    if data_de_nascimento:
        # Converta a data de nascimento para o formato desejado
        data_de_nascimento = datetime.strptime(data_de_nascimento, "%a, %d %b %Y %H:%M:%S %Z").strftime("%d/%m/%Y")

    toast_script = """
        <script>
            Toastify({
                text: "Login feito com sucesso! Bem vindo",
                duration: 5000,
                gravity: "top",
                backgroundColor: "green"
            }).showToast();
        </script>
    """

    saldo = funcoes.saldo(db,cpf)
    return render_template("login-form-18/Profile.html", nome=nome, data_de_nascimento=data_de_nascimento, saldo=saldo, toast_script=toast_script)

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
        
        if not funcoes.verificar_cpf(db,cpf) and not funcoes.verificar_user(db,username):
            

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
        else:
            toast_script = """
                <script>
                    Toastify({
                        text: "Usuário Ja existente",
                        duration: 5000,  // Duração do toast em milissegundos (opcional)
                        gravity: "top",  // Posição do toast (opcional)
                        backgroundColor: "red"  // Cor de fundo do toast (opcional)
                    }).showToast();
                </script>
                """
            return render_template('login-form-18/Cadastro.html',toast_script=toast_script)


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
        return redirect('profile', toast_script=toast_script)

    # Certifique-se de fechar a conexão e o cursor mesmo se não houver um envio POST
    cursor.close()
    db.close()

    return render_template('login-form-18/reset_password.html')


@app.route('/Sacar')
def sacar():
    cpf = session.get('cpf', None)
    if cpf != 0:
        return render_template("Inside/saque.html")


@app.route('/Saque',methods=['POST'])
def saque():
    db = conectar_banco()
    # Recupere os dados da sessão
    nome = session.get('nome', None)
    data_de_nascimento = session.get('data_de_nascimento', None)
    cpf = session.get('cpf', None)

    if data_de_nascimento:
        # Converta a data de nascimento para o formato desejado
        data_de_nascimento = datetime.strptime(data_de_nascimento, "%a, %d %b %Y %H:%M:%S %Z").strftime("%d/%m/%Y")
    if request.method == 'POST':
        saldo = funcoes.saldo(db,cpf)
        valor_saque = float(request.form['valor'])
        if(valor_saque < saldo):
            funcoes.saque(db,cpf,valor_saque)
             #valor nao disponivel 
            nomecom = nome
            dt_nasc = data_de_nascimento
            saldo = funcoes.saldo(db,cpf)
            toast_script = """
            <script>
                Toastify({
                    text: "Saque realizado com sucesso",
                    duration: 5000,  // Duração do toast em milissegundos (opcional)
                    gravity: "top",  // Posição do toast (opcional)
                    backgroundColor: "green"  // Cor de fundo do toast (opcional)
                }).showToast();
            </script>
            """
            return render_template('login-form-18/Profile.html', toast_script=toast_script,saldo = saldo,data_de_nascimento = dt_nasc,nome=nomecom)
        else:
            #valor nao disponivel 
            # Adicione o script para mostrar um toast
            toast_script = """
            <script>
                Toastify({
                    text: "Saldo Insuficiente",
                    duration: 5000,  // Duração do toast em milissegundos (opcional)
                    gravity: "top",  // Posição do toast (opcional)
                    backgroundColor: "red"  // Cor de fundo do toast (opcional)
                }).showToast();
            </script>
            """
            return render_template('Inside/saque.html', toast_script=toast_script)






@app.route('/Depositar')
def depositar():
        return render_template("Inside/deposito.html")


@app.route('/Deposito',methods=['POST'])
def deposito():
    db = conectar_banco()
    # Recupere os dados da sessão
    nome = session.get('nome', None)
    data_de_nascimento = session.get('data_de_nascimento', None)
    cpf = session.get('cpf', None)

    if data_de_nascimento:
        # Converta a data de nascimento para o formato desejado
        data_de_nascimento = datetime.strptime(data_de_nascimento, "%a, %d %b %Y %H:%M:%S %Z").strftime("%d/%m/%Y")
    if request.method == 'POST':
        saldo = funcoes.saldo(db,cpf)
        valor_saque = float(request.form['valor'])
        funcoes.deposito(db,cpf,valor_saque)
         #valor nao disponivel 
        nomecom = nome
        dt_nasc = data_de_nascimento
        saldo = funcoes.saldo(db,cpf)
        toast_script = """
        <script>
            Toastify({
                text: "Saque realizado com sucesso",
                duration: 5000,  // Duração do toast em milissegundos (opcional)
                gravity: "top",  // Posição do toast (opcional)
                backgroundColor: "green"  // Cor de fundo do toast (opcional)
            }).showToast();
        </script>
        """
        return render_template('login-form-18/Profile.html', toast_script=toast_script,saldo = saldo,data_de_nascimento = dt_nasc,nome=nomecom)

if __name__ == '__main__':
    app.run(debug=True)
