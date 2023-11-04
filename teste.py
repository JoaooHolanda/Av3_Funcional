import bcrypt

# Gere uma senha aleatória
password = "minha_senha_insegura".encode('utf-8')

# Crie um hash para a senha
hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed_password)
# Verifique a senha em algum momento posterior
input_password = "minha_senha_insegura".encode('utf-8')
if bcrypt.checkpw(input_password, hashed_password):
    print("Senha correta!")
else:
    print("Senha incorreta.")
