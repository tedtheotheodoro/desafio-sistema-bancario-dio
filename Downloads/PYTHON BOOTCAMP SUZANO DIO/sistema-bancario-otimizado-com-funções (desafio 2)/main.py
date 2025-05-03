from usuario import Usuario
from conta import ContaCorrente
import operacoes  

# Criar um usuário
usuario1 = Usuario("João Silva", "1985-05-14", "12345678900", "Rua A, 123 - São Paulo/SP")
print(f"Usuário {usuario1.nome} criado com sucesso!")

# Criar uma conta para esse usuário
conta1 = ContaCorrente("0001", 1, usuario1)
usuario1.adicionar_conta(conta1)
print(f"Conta {conta1.numero_conta} criada para o usuário {usuario1.nome}.")

# Realizar um depósito
operacoes.depositar(conta1, 1000)
print(f"Saldo após depósito: R${conta1.saldo}")

# Realizar um saque
operacoes.sacar(conta1, 200)
print(f"Saldo após saque: R${conta1.saldo}")

# Visualizar o extrato
extrato = operacoes.visualizar_extrato(conta1)
print("Extrato da conta:")
for transacao in extrato:
    print(transacao)