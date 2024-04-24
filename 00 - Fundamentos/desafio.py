
import textwrap

def menu ():
    menu = """\n
            MENU
\t[1] Depositar\t[4] Novo Usuário
\t[2] Sacar\t[5] Nova Conta
\t[3] Extrato\t[6] Listar Contas
\t\t[7] Sair 
=> """
    return input(textwrap.dedent(menu))    
#Tudo andes do / precisa ser passado por posição
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: +R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!")
    else:
        print("Valor inválido, não foi possível realizar depósito.")

    return saldo, extrato
#tudo que vem * depois do * precisa ser passado de forma nomeada
def saque(*,saldo, valor, extrato, limite, numero_saques, limite_saques):
    #O sistema só deve permitir 3 saques diários
    if numero_saques >= limite_saques:
        print("Operação falhou! Número de saques diário foi excedido.")
    #O valor máximo de saque é R$ 500,00
    elif valor > limite:
        print(f"Operação falhou! O valor do saque excede R$ {limite:.2f}.")
    #Verifica saldo insuficiente
    elif valor > saldo:
        print("Operação falhou! Saldo insuficiente.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: -R$ {valor:.2f}\n"
        numero_saques += 1
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def exibir_extrato(saldo, /,*,extrato):
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\n\tSaldo: \t\tR$ {saldo:.2f}")
        print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Digite seu cpf(digite somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print("Já existe usuário cadastrado nesse cpf")
        return
    
    nome = input("Digite seu nome: ")
    data_nascimento = input("Digite a data do seu nascimento(dd-mm-aaaa): ")
    endereco = input("Digite seu endereço completo(logradouro, n - bairro - cidade/sigla estado) : ")
    
    usuarios.append({"nome":nome, "data_nascimento": data_nascimento, "cpf":cpf, "endereço":endereco})
    
    print("usuário criado com sucesso")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia,numero_conta, usuarios):    
    cpf = input("Digite seu cpf(digite somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("Conta criada com sucesso")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    print("Usuário não encontrada, não foi possível criar conta")
    
def listar_contas(contas):
    for conta in contas:
        texto = f"""\
            Agência: \t\t{conta['agencia']}
            Conta Corrente: \t{conta['numero_conta']}
            Titular: \t\t{conta['usuario']['nome']}
        """
        print("*"*100)
        print(textwrap.dedent(texto))
        print("*"*100)
            
def main():
    LIMITE_SAQUES = 3
    LIMITE = 500
    AGENCIA = "0001"

    saldo = 0
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []


    while True:
        opcao = menu()
        
        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))
            #Permite apenas valores positivo de depósito
            saldo, extrato = depositar(saldo, valor, extrato)
        elif opcao == "2":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato = saque(saldo = saldo,
                valor= valor,
                extrato= extrato,
                limite= LIMITE,
                numero_saques= numero_saques,
                limite_saques= LIMITE_SAQUES
                )
        elif opcao == "3":
            exibir_extrato(saldo, extrato= extrato)
        elif opcao == "4":
            criar_usuario(usuarios)
        elif opcao == "5":      
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            
            if(conta):
                contas.append(conta)
                
        elif opcao == "6":
            listar_contas(contas)
        elif opcao ==  "7":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()