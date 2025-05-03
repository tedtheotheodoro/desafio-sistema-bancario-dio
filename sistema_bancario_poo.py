import abc
from datetime import datetime

# --- Classes de Transacao ---

# Interface ou Classe Base Abstrata para Transações
class Transacao(abc.ABC):
    @property
    @abc.abstractproperty
    def valor(self):
        pass

    @abc.abstractmethod
    def registrar(self, conta):
        pass

# Classe para Depósito
class Deposito(Transacao):
    def __init__(self, valor):
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser positivo.")
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
        return sucesso # Retorna se a transação foi bem sucedida

# Classe para Saque
class Saque(Transacao):
    def __init__(self, valor):
        if valor <= 0:
            raise ValueError("O valor do saque deve ser positivo.")
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
        return sucesso # Retorna se a transação foi bem sucedida

# --- Classe Historico ---

class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        # Registra a transação e a data/hora
        self._transacoes.append({
            "tipo": type(transacao).__name__, # Nome da classe (Deposito ou Saque)
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })

    @property
    def transacoes(self):
        return self._transacoes

# --- Classes de Cliente ---

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = [] # Uma lista para armazenar as contas do cliente

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        # Verifica se a conta pertence a este cliente
        if conta not in self.contas:
            print("\n@@@ Erro: A conta informada não pertence a este cliente! @@@")
            return False

        # Delega a execução da transação para o objeto transacao
        return transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf # CPF pode ser usado como identificador único

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001" # Agência fixa por enquanto
        self._cliente = cliente # Associa a conta a um cliente
        self._historico = Historico() # Cada conta tem seu próprio histórico

    @classmethod
    def nova_conta(cls, cliente, numero):
        # Método de classe para criar uma nova conta, associando-a a um cliente
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False

        elif valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        else:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques # Limite de saques por transação (não total)
        self._saques_hoje = 0 # Contador de saques diários

    def sacar(self, valor):
        excedeu_limite = valor > self.limite
        excedeu_saques = self._saques_hoje >= self.limite_saques # Verifica limite diário

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite por saque. @@@")
            return False

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques diários excedido. @@@")
            return False

        # Chama o método sacar da superclasse para realizar o saque se as validações passarem
        if super().sacar(valor):
            self._saques_hoje += 1
            return True
        return False
    
def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [lu]\tListar usuários
    [q]\tSair
    => """
    return input(menu)

# Funções auxiliares para buscar cliente e conta
def filtrar_cliente(cpf, clientes):
    # Busca um cliente na lista pelo CPF
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def filtrar_conta(numero_conta, contas):
    # Busca uma conta na lista pelo número
    for conta in contas:
        if conta.numero == numero_conta:
            return conta
    return None

def recuperar_conta_cliente(cliente):
    # Retorna a primeira conta do cliente (para simplificar por enquanto)
    # Em um sistema real, precisaria permitir escolher entre múltiplas contas
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    return cliente.contas[0] # Retorna a primeira conta encontrada

# --- Funções de Operação ---

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            print(f"{transacao['tipo']}: R$ {transacao['valor']:.2f} ({transacao['data']})")

    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com o CPF informado! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ") # Pode adicionar validação de formato
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    novo_cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(novo_cliente)

    print("\n=== Cliente criado com sucesso! ===")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    # Cria a nova conta corrente e a associa ao cliente
    nova_conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(nova_conta)
    cliente.adicionar_conta(nova_conta) # Adiciona a conta à lista de contas do cliente

    print("\n=== Conta criada com sucesso! ===")

def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return

    print("\n============= Contas Cadastradas =============")
    for conta in contas:
        # Exibe informações da conta e do cliente associado
        print(f"Agência:\t{conta.agencia}")
        print(f"Conta Corrente:\t{conta.numero}")
        print(f"Titular:\t{conta.cliente.nome}")
        print(f"CPF:\t\t{conta.cliente.cpf}")
        print("--------------------------------------------")
    print("==============================================")

def listar_usuarios(clientes):
    if not clientes:
        print("\n@@@ Nenhum usuário cadastrado. @@@")
        return

    print("\n============= Usuários Cadastrados =============")
    for cliente in clientes:
        # Exibe informações básicas do cliente
        print(f"Nome:\t\t{cliente.nome}")
        print(f"CPF:\t\t{cliente.cpf}")
        print(f"Endereço:\t{cliente.endereco}")
        print("--------------------------------------------")
    print("==============================================")

# --- Programa Principal ---

def main():
    clientes = [] # Lista para armazenar objetos Cliente/PessoaFisica
    contas = []   # Lista para armazenar objetos Conta/ContaCorrente
    numero_conta = 1 # Contador para gerar números de conta únicos

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            criar_conta(numero_conta, clientes, contas)
            numero_conta += 1 # Incrementa o número da conta para a próxima criação

        elif opcao == "lu":
            listar_usuarios(clientes)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

# Executa o programa principal
if __name__ == "__main__":
    main()