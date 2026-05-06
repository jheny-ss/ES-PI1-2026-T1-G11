from models.elector import *
from models.candidate import *
from models.voting import *
from models.validators.voter_registration_validation import registration_validation
from models.validators.cpf_validation import validate_cpf
from views.menus import *
from models.voting import cast_vote

# =========================
# SISTEMA PRINCIPAL
# =========================

def run_system():
    """
    Executa o sistema principal.

    Exibe o menu principal continuamente e direciona o usuário
    para os módulos de gerenciamento, votação ou encerramento do sistema.
    """
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
    """
    Controla o fluxo do módulo de gerenciamento.

    Permite ao usuário acessar as funcionalidades de
    gerenciamento de eleitores ou candidatos.
    """
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
    """
    Controla o fluxo do menu de eleitores.

    Permite listar, buscar, remover, editar e cadastrar eleitores.
    """
    while True:
        choice = elector_menu()

        match choice:
            case 1:
                list_electors()

            case 2:
                cpf = input("CPF: ")
                elector = get_elector_by_cpf(cpf)
                print(elector if elector else "Não encontrado!")

            case 3:
                cpf = input("CPF: ")
                delete_elector(cpf)

            case 4:
                update_elector()

            case 5:
                name = input("Nome: ")
                cpf = input("CPF: ")

                # Validação imediata do CPF
                if not validate_cpf(cpf):
                  print("CPF inválido!")
                  input("\nENTER para continuar...")
                  continue

                voter_id = input("Título: ")

                # Valida o título de eleitor
                if not registration_validation(voter_id):
                    print("Título de eleitor inválido!")

                # Verifica duplicidade
                elif elector_exists(cpf, voter_id):
                    print("CPF ou título já cadastrado!")

                else:
                    is_poll_worker_input = input("É mesário? (Sim/Não): ")
                    is_poll_worker = True if is_poll_worker_input == "Sim" else False

                    access_key = generate_access_key()
                    print("Chave:", access_key)

                    create_elector(name, cpf, voter_id, access_key, is_poll_worker)

            case 6:
                return

            case _:
                print("Opção inválida!")

        input("\nENTER para continuar...")


# =========================
# CANDIDATOS
# =========================

def handle_candidates():
    """
    Controla o fluxo do menu de candidatos.

    Permite listar, buscar, remover, editar e cadastrar candidatos.
    """
    while True:
        choice = candidate_menu()

        match choice:
            case 1:
                list_candidates()

            case 2:
                number = input("Número: ")
                candidate = get_candidate_by_number(number)
                print(candidate if candidate else "Não encontrado!")

            case 3:
                number = input("Número: ")
                delete_candidate(number)

            case 4:
                update_candidate()

            case 5:
                name = input("Nome: ")
                number = input("Número: ")
                party = input("Partido: ")

                create_candidate(name, number, party)

            case 6:
                return

            case _:
                print("Opção inválida!")

        input("\nENTER para continuar...")


# =========================
# VOTAÇÃO
# =========================

def handle_voting():
    """
    Controla o fluxo do módulo de votação.

    Permite autenticar o mesário, iniciar a votação,
    acessar auditoria e visualizar resultados.
    """
    while True:
        choice = voting_menu()

        match choice:
            case 1:
                voter_id = input("Título: ")
                cpf_partial = input("4 primeiros dígitos do CPF: ")
                access_key = input("Chave: ")

                if validate_poll_worker(cpf_partial, voter_id, access_key):
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
    voting_open = True
    """
    Controla o fluxo da votação aberta.

    Permite registrar votos e encerrar o processo de votação.
    """
    while voting_open:
        choice = open_voting_menu()

        match choice:
            case 1:
                cast_vote()

            case 2:
                print("Encerrando votação...")
                voting_open = False

            case 3:
                voting_open = False

            case _:
                print("Opção inválida!")

        if voting_open:
            input("\nENTER para continuar...")

# =========================
# RESULTADOS
# =========================

def handle_results():
    """
    Controla o fluxo do módulo de resultados.

    Permite visualizar boletim de urna, estatísticas,
    votos por partido e validação de integridade.
    """
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
    """
    Controla o fluxo do módulo de auditoria.

    Permite visualizar logs do sistema e protocolos de votação.
    """
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
