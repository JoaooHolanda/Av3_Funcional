import re

# Dicionário de padrões de complexidade
padroes = {
    "baixa": r"^(?:\d{1,6}|[A-Za-z]{1,6})$",
    "média": r"^[a-zA-Z]*\d[a-zA-Z]*|[a-zA-Z]*\d[a-zA-Z]*$",
    "alta": r"^(?=.*[A-Z])(?=.*\d)(?=.*[:!@#$%¨&*()])[a-zA-Z\d:!@#$%¨&*()]+$",
}

# Função lambda para verificar complexidade de senha
verificar_complexidade_senha = lambda senha, nivel: (
    next((nivel for padrao_nivel, padrao in padroes.items() if re.search(padrao, senha) and padrao_nivel == nivel), None)
)
