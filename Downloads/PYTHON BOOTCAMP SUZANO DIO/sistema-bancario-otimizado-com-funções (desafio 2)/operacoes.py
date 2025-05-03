def depositar(conta, valor):
    """Função para realizar depósito na conta."""
    conta.deposito(valor)
    
def sacar(conta, valor):
    """Função para realizar saque da conta."""
    conta.saque(valor)
    
def visualizar_extrato(conta):
    """Função para exibir o extrato da conta."""
    return conta.extrato