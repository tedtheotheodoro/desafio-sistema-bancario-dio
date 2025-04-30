class ContaCorrente:
    def __init__(self, numero_conta, agencia, usuario):
        self.numero_conta = numero_conta
        self.agencia = agencia
        self.usuario = usuario
        self.saldo = 0
        self.extrato = []
        
    def deposito(self, valor):
        self.saldo += valor
        self.extrato.append(f"Depósito: R${valor}")
        
    def saque(self, valor):
        if self.saldo >= valor:
            self.saldo -= valor
            self.extrato.append(f"Saque: R${valor}")
        else:
            print("Saldo insuficiente para realizar o saque.")
    
    def verificar_saldo(self):
        return self.saldo

    def transferir(self, valor, conta_destino):
        if self.saldo >= valor:
            self.saque(valor)
            conta_destino.deposito(valor)
            self.extrato.append(f"Transferência para conta {conta_destino.numero_conta}: R${valor}")
            print(f"Transferência de R${valor} realizada com sucesso!")
        else:
            print("Saldo insuficiente para realizar a transferência.")
    
    def exibir_extrato(self):
        print(f"Extrato da conta {self.numero_conta}:")
        for transacao in self.extrato:
            print(transacao)
