class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []  # lista para armazenar as contas associadas ao usuário

    def adicionar_conta(self, conta):
        self.contas.append(conta)
