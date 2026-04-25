from models.elector import *
from models.candidate import *
from models.voting import *

from views.menus import *

# =========================
# SISTEMA PRINCIPAL
# =========================

def run_system():
    while True:
        choice = main_menu()

        match choice:
            case 1:
                handle_management()
            case 2:
                handle_voting()
            case 3:
                print("Encerrando sistema...")
                break
            case _:
                print("Opção inválida!")


# =========================
# GERENCIAMENTO
# =========================

def handle_management():
    while True:
        choice = management_menu()

        match choice:
            case 1:
                handle_electors()
            case 2:
                handle_candidates()
            case 3:
                return
            case _:
                print("Opção inválida!")


# =========================
# ELEITORES
# =========================

def handle_electors():
    while True:
        choice = elector_menu()

        match choice:
            case 1:
                listar_eleitores()

            case 2:
                cpf = input("CPF: ")
                eleitor = buscar_eleitor(cpf)
                print(eleitor if eleitor else "Não encontrado!")

            case 3:
                cpf = input("CPF: ")
                remover_eleitor(cpf)

            case 4:
                editar_eleitor()

            case 5:
                nome = input("Nome: ")
                cpf = input("CPF: ")
                titulo = input("Título: ")

                if eleitor_existe(cpf, titulo):
                    print("CPF ou título já cadastrado!")
                else:
                    resp = input("É mesário? (Sim/Não): ")
                    status = True if resp == "Sim" else False

                    chave = gerar_chave_acesso()
                    print("Chave:", chave)

                    inserir_eleitor(nome, cpf, titulo, chave, status)

            case 6:
                return

            case _:
                print("Opção inválida!")

        input("\nENTER para continuar...")


# =========================
# CANDIDATOS
# =========================

def handle_candidates():
    while True:
        choice = candidate_menu()

        match choice:
            case 1:
                listar_candidatos()

            case 2:
                numero = input("Número: ")
                candidato = buscar_candidato(numero)
                print(candidato if candidato else "Não encontrado!")

            case 3:
                numero = input("Número: ")
                remover_candidato(numero)

            case 4:
                editar_candidato()

            case 5:
                nome = input("Nome: ")
                numero = input("Número: ")
                partido = input("Partido: ")

                inserir_candidato(nome, numero, partido)

            case 6:
                return

            case _:
                print("Opção inválida!")

        input("\nENTER para continuar...")


# =========================
# VOTAÇÃO
# =========================

def handle_voting():
    while True:
        choice = voting_menu()

        match choice:
            case 1:
                titulo = input("Título: ")
                cpf = input("4 primeiros dígitos do CPF: ")
                chave = input("Chave: ")

                if validar_mesario(cpf, titulo, chave):
                    print("Acesso autorizado!")
                    zeresima()
                    handle_open_voting()
                else:
                    print("Acesso negado!")

            case 2:
                handle_audit()

            case 3:
                handle_results()

            case 4:
                return

            case _:
                print("Opção inválida!")

        input("\nENTER para continuar...")


# =========================
# VOTAÇÃO ABERTA
# =========================

def handle_open_voting():
    while True:
        choice = open_voting_menu()

        match choice:
            case 1:
                print("Processando voto...")

            case 2:
                print("Encerrando votação...")
                return

            case 3:
                return

            case _:
                print("Opção inválida!")

        input("\nENTER para continuar...")


# =========================
# RESULTADOS
# =========================

def handle_results():
    while True:
        choice = results_menu()

        match choice:
            case 1:
                print("Boletim de urna...")

            case 2:
                print("Estatísticas...")

            case 3:
                print("Votos por partido...")

            case 4:
                print("Validação de integridade...")

            case 5:
                return

            case _:
                print("Opção inválida!")

        input("\nENTER para continuar...")


# =========================
# AUDITORIA
# =========================

def handle_audit():
    while True:
        choice = audit_menu()

        match choice:
            case 1:
                print("Logs...")

            case 2:
                print("Protocolos...")

            case 3:
                return

            case _:
                print("Opção inválida!")

        input("\nENTER para continuar...")