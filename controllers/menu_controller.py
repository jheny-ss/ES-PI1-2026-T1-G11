from models.elector import *
from models.candidate import *
from models.voting import *
from models.validators.voter_registration_validation import registration_validation
from models.validators.cpf_validation import validate_cpf
from models.validators.name_validation import validate_full_name
from views.menus import *

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
                while not validate_cpf(cpf):
                    print("CPF inválido!")
                    cpf = input("CPF: ")

                elector = get_elector_by_cpf(cpf)
                print(elector if elector else "Não encontrado!")

            case 3:
                cpf = input("CPF do eleitor: ")
                while not validate_cpf(cpf):
                    print("CPF inválido!")
                    cpf = input("CPF do eleitor: ")

                delete_elector(cpf)

            case 4:
                elector = None

                while not elector:

                    cpf = input("CPF do eleitor: ")

                    while not validate_cpf(cpf):
                        print("CPF inválido!")
                        cpf = input("CPF do eleitor: ")

                    elector = get_elector_by_cpf(cpf)

                    if not elector:
                        print("Eleitor não encontrado!")

                name = input("Novo nome: ")

                while not validate_full_name(name):
                    print("Nome inválido!")
                    name = input("Novo nome: ")

                voter_id = input("Novo título: ")

                while not registration_validation(voter_id):
                    print("Título inválido!")
                    voter_id = input("Novo título: ")

                is_poll_worker_input = input("Status de Mesário (Sim/Não): ")

                while is_poll_worker_input not in ["Sim", "Não"]:
                    print("Entrada inválida!")
                    is_poll_worker_input = input("Status de Mesário (Sim/Não): ")

                is_poll_worker = is_poll_worker_input == "Sim"

                update_elector_db(cpf, name, voter_id, is_poll_worker)

                print("Eleitor atualizado com sucesso!")

            case 5:
                
                name = input("Nome: ")
                while not validate_full_name(name):
                    print("Nome inválido! Digite nome e sobrenome.")
                    name = input("Nome: ")

               
                cpf = input("CPF: ")
                while not validate_cpf(cpf):
                    print("CPF inválido!")
                    cpf = input("CPF: ")

                
                voter_id = input("Título: ")
                while not registration_validation(voter_id):
                    print("Título inválido!")
                    voter_id = input("Título: ")

                connection, cursor = get_cursor()

                try:
                    if elector_exists(cursor, cpf, voter_id):
                        print("CPF ou título já cadastrado!")
                        continue

                    
                    is_poll_worker_input = input("É mesário? (Sim/Não): ")
                    while is_poll_worker_input not in ["Sim", "Não"]:
                        print("Entrada inválida!")
                        is_poll_worker_input = input("É mesário? (Sim/Não): ")

                    is_poll_worker = is_poll_worker_input == "Sim"

                    access_key = generate_access_key(name)
                    print("Chave gerada:", access_key)

                    create_elector(cursor, name, cpf, voter_id, access_key, is_poll_worker)
                    connection.commit()

                    print("Eleitor cadastrado com sucesso!")

                finally:
                    cursor.close()
                    connection.close()

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
    """

    while True:
        while True:
            choice = candidate_menu()

            if isinstance(choice, int) and 1 <= choice <= 6:
                break

            print("Opção inválida! Digite novamente.\n")

        match choice:
            case 1:
                list_candidates()

            case 2:
                while True:
                    number = input("Número (ou 0 para voltar): ")

                    if number == "0":
                        break

                    candidate = get_candidate_by_number(number)

                    if candidate:
                        print(candidate)
                        break
                    else:
                        print("Não encontrado! Tente novamente.\n")

            case 3:
                    while True:
                        number = input("Número (ou 0 para voltar): ")

                        if number == "0":
                            break

                        candidate = get_candidate_by_number(number)

                        if not candidate:
                            print("Candidato não encontrado!\n")
                            continue

                        confirm = input("Confirma remoção? (s/n): ").lower()

                        if confirm == "s":
                            delete_candidate(number)
                        else:
                            print("Remoção cancelada.")

                        break

            case 4:
                update_candidate()

            case 5:
                name = input("Nome: ")
                number = input("Número: ")
                party = input("Partido: ")

                create_candidate(name, number, party)

            case 6:
                return

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
    """
    Controla o fluxo da votação aberta.

    Permite registrar votos e encerrar o processo de votação.
    """
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
