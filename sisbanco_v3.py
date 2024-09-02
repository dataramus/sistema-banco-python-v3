#Esse código foi projetado para ser simples e didático, ideal para quem está aprendendo os conceitos de programação orientada a objetos 
#e quer entender como construir um programa básico que simula operações bancárias.

# Importa o módulo textwrap, que é usado para manipular texto e remover indentação desnecessária.
import textwrap  

# Definindo uma classe para representar um usuário do banco
class Usuario:
    # O método __init__ é o construtor da classe e é chamado quando criamos um novo objeto Usuario.
    # Ele inicializa os atributos do usuário como nome, data de nascimento, CPF e endereço.
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

    @staticmethod
    def criar_usuario(usuarios):
        # Cria um novo usuário e o adiciona à lista de usuários.
        cpf = input("Informe o CPF (somente número): ")
        # Verifica se já existe um usuário com o CPF informado.
        if Usuario.filtrar_usuario(cpf, usuarios):
            print("\n@@@ Já existe usuário com esse CPF! @@@")
            return None

        # Solicita os demais dados do usuário.
        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        
        # Cria um novo objeto Usuario e o adiciona à lista de usuários.
        novo_usuario = Usuario(nome, data_nascimento, cpf, endereco)
        usuarios.append(novo_usuario)
        print("=== Usuário criado com sucesso! ===")
        return novo_usuario

    @staticmethod
    # Filtra os usuários na lista pelo CPF.
    def filtrar_usuario(cpf, usuarios):
        for usuario in usuarios:
            if usuario.cpf == cpf:
                return usuario
        return None


# Definindo uma classe para representar uma conta bancária
class Conta:
    # Construtor da classe Conta, inicializa os atributos de uma conta como agência, número da conta,
    # titular (que é um objeto Usuario), saldo, limite, extrato e número de saques.
    def __init__(self, agencia, numero_conta, usuario):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.saldo = 0
        self.limite = 500
        self.extrato = ""
        self.numero_saques = 0
        self.LIMITE_SAQUES = 3

    # Deposita um valor na conta.
    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            # Registra o depósito no extrato.
            self.extrato += f"Depósito:\tR$ {valor:.2f}\n" 
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    # Saca um valor da conta, considerando várias verificações.
    def sacar(self, valor):
        if valor > self.saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > self.limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif self.numero_saques >= self.LIMITE_SAQUES:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        elif valor > 0:
            self.saldo -= valor
            # Registra o saque no extrato.
            self.extrato += f"Saque:\t\tR$ {valor:.2f}\n" 
            self.numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    # Exibi o extrato da conta, mostrando todas as transações realizadas.
    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not self.extrato else self.extrato)
        print(f"\nSaldo:\t\tR$ {self.saldo:.2f}")
        print("==========================================")


# Definindo uma classe para representar o banco, que gerencia contas e usuários
class Banco:
    # Construtor da classe Banco, inicializa as listas de usuários e contas, e define a agência padrão.
    def __init__(self):
        self.usuarios = []
        self.contas = []
        self.AGENCIA = "0001"

    # Criar uma nova conta para um usuário existente.
    def criar_conta(self):
        cpf = input("Informe o CPF do usuário: ")
        usuario = Usuario.filtrar_usuario(cpf, self.usuarios)
        # Número da conta é definido com base na quantidade de contas existentes.
        if usuario:
            numero_conta = len(self.contas) + 1 
            conta = Conta(self.AGENCIA, numero_conta, usuario)
            self.contas.append(conta)
            print("\n=== Conta criada com sucesso! ===")
            return conta
        print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
        return None

    # Listar todas as contas existentes no banco.
    def listar_contas(self):
        for conta in self.contas:
            linha = f"""\
                Agência:\t{conta.agencia}
                C/C:\t\t{conta.numero_conta}
                Titular:\t{conta.usuario.nome}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))


# Função para exibir o menu e capturar a escolha do usuário
def menu():
    menu_text = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_text))


# Função principal que controla o fluxo do programa
def main():
    # Cria um objeto Banco que gerencia os usuários e contas.
    banco = Banco()  

    # Loop que só termina quando o usuário escolher sair (opção "q").
    while True:  
        # Exibe o menu e captura a escolha do usuário.
        opcao = menu()  

        # Caso o usuário escolha depositar dinheiro em uma conta.
        if opcao == "d":
            numero_conta = int(input("Informe o número da conta: "))
            conta = banco.contas[numero_conta - 1]
            valor = float(input("Informe o valor do depósito: "))
            conta.depositar(valor)

        # Caso o usuário escolha sacar dinheiro de uma conta.
        elif opcao == "s":
            numero_conta = int(input("Informe o número da conta: "))
            conta = banco.contas[numero_conta - 1]
            valor = float(input("Informe o valor do saque: "))
            conta.sacar(valor)

        # Caso o usuário escolha exibir o extrato de uma conta.
        elif opcao == "e":
            numero_conta = int(input("Informe o número da conta: "))
            conta = banco.contas[numero_conta - 1]
            conta.exibir_extrato()

        # Caso o usuário escolha criar um novo usuário.
        elif opcao == "nu":
            Usuario.criar_usuario(banco.usuarios)

        # Caso o usuário escolha criar uma nova conta.
        elif opcao == "nc":
            banco.criar_conta()

        # Caso o usuário escolha listar todas as contas.
        elif opcao == "lc":
            banco.listar_contas()

        # Caso o usuário escolha sair do programa.
        elif opcao == "q":
            break

        # Caso o usuário digite uma opção inválida.
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


# Chama a função principal para iniciar o programa.
if __name__ == "__main__":
    main() 
