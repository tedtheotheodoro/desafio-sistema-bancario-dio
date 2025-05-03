saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

def depositar(valor):
    global saldo
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
    else:
        print("Valor de depósito inválido. O valor deve ser positivo.")

def sacar(valor):
    global saldo, numero_saques
    if valor > saldo:
        print("Saldo insuficiente para saque!")
    elif numero_saques >= LIMITE_SAQUES:
        print("Limite de saques diário atingido!")
    elif valor > limite:
        print(f"O limite para saques diários é de R$ {limite:.2f}.")
    else:
        saldo -= valor
        numero_saques += 1
        extrato.append(f"Saque: R$ {valor:.2f}")
        print(f"Saque de R$ {valor:.2f} realizado com sucesso.")

def extrato_func():
    print("\nExtrato:")
    if not extrato:
        print("Nenhuma transação realizada.")
    else:
        for transacao in extrato:
            print(transacao)
    print(f"Saldo final: R$ {saldo:.2f}")

def menu():
    return """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
"""

while True:
    print("\nBem-vindo ao sistema bancário.")
    opcao = input(menu())
    
    if opcao == "d":
        try:
            valor = float(input("Digite o valor a ser depositado: R$ "))
            depositar(valor)
        except ValueError:
            print("Entrada inválida! Por favor, insira um número válido.")
    elif opcao == "s":
        try:
            valor = float(input("Digite o valor a ser sacado: R$ "))
            sacar(valor)
        except ValueError:
            print("Entrada inválida! Por favor, insira um número válido.")
    elif opcao == "e":
        extrato_func()
    elif opcao == "q":
        print("Saindo do sistema. Até logo!")
        break
    else:
        print("Opção inválida! Escolha novamente.")
