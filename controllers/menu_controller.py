from models.elector import *
from models.candidate import *
from models.voting import *
from models.validators.voter_registration_validation import (
    registration_validation
)
from models.validators.cpf_validation import (
    validate_cpf
)
from models.validators.name_validation import (
    validate_full_name
)
from models.utils.input_helpers import (
    input_with_exit,
    input_yes_no
)
from views.menus import *
from models.voting import cast_vote
from models.audit import (
    show_logs,
    show_protocols,
    register_opening_log
)
from models.results import elector_choice
from models.results import *
# =========================
# SISTEMA PRINCIPAL
# =========================

def run_system():
    """
    Executa o sistema principal.

    Exibe o menu principal continuamente e direciona o usuário
    para os módulos de gerenciamento, votação ou encerramento
    do sistema.
    """

    system_running = True

    while system_running:

        choice = main_menu()

        match choice:

            case 1:
                handle_management()

            case 2:
                handle_voting()

            case 3:
                print("Encerrando sistema...")
                system_running = False

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

    management_running = True

    while management_running:

        choice = management_menu()

        match choice:

            case 1:
                handle_electors()

            case 2:
                handle_candidates()

            case 3:
                management_running = False

            case _:
                print("Opção inválida!")

# =========================
# ELEITORES
# =========================

def handle_electors():
    """
    Controla o fluxo do menu de eleitores.

    Permite listar, buscar, remover, editar
    e cadastrar eleitores.
    """

    elector_running = True

    while elector_running:

        choice = elector_menu()

        match choice:
            case 1:
                list_electors()
            case 2:

                cpf = input_with_exit(
                    "CPF",
                    validate_cpf,
                    "CPF inválido!"
                )

                if cpf is not None:

                    elector = (
                        get_elector_by_cpf(cpf)
                    )

                    print(
                        elector
                        if elector
                        else "Não encontrado!"
                    )
            case 3:

                cpf = input_with_exit(
                    "CPF do eleitor",
                    validate_cpf,
                    "CPF inválido!"
                )

                if cpf is not None:
                    delete_elector(cpf)
            case 4:

                elector = None

                while elector is None:

                    cpf = input_with_exit(
                        "CPF do eleitor",
                        validate_cpf,
                        "CPF inválido!"
                    )

                    if cpf is None:
                        break

                    elector = (
                        get_elector_by_cpf(cpf)
                    )

                    if not elector:
                        print(
                            "Eleitor não encontrado!"
                        )

                if elector is not None:

                    name = input_with_exit(
                        "Novo nome",
                        validate_full_name,
                        "Nome inválido!"
                    )

                    if name is None:
                        continue

                    voter_id = input_with_exit(
                        "Novo título",
                        registration_validation,
                        "Título inválido!"
                    )

                    if voter_id is None:
                        continue

                    is_poll_worker = (
                        input_yes_no(
                            "Status de Mesário"
                        )
                    )

                    if is_poll_worker is None:
                        continue

                    update_elector_db(
                        cpf,
                        name,
                        voter_id,
                        is_poll_worker
                    )

                    print(
                        "Eleitor atualizado "
                        "com sucesso!"
                    )
            case 5:

                name = input_with_exit(
                    "Nome",
                    validate_full_name,
                    (
                        "Nome inválido! "
                        "Digite nome e sobrenome."
                    )
                )

                if name is None:
                    continue

                cpf = input_with_exit(
                    "CPF",
                    validate_cpf,
                    "CPF inválido!"
                )

                if cpf is None:
                    continue

                voter_id = input_with_exit(
                    "Título",
                    registration_validation,
                    "Título inválido!"
                )

                if voter_id is None:
                    continue

                connection, cursor = get_cursor()

                try:

                    if elector_exists(
                        cursor,
                        cpf,
                        voter_id
                    ):
                        print(
                            "CPF ou título "
                            "já cadastrado!"
                        )

                    else:

                        is_poll_worker = (
                            input_yes_no(
                                "É mesário?"
                            )
                        )

                        if is_poll_worker is None:
                            continue

                        access_key = (
                            generate_access_key(name)
                        )

                        print(
                            "Chave gerada:",
                            access_key
                        )

                        create_elector(
                            cursor,
                            name,
                            cpf,
                            voter_id,
                            access_key,
                            is_poll_worker
                        )

                        connection.commit()

                        print(
                            "Eleitor cadastrado "
                            "com sucesso!"
                        )

                finally:
                    cursor.close()
                    connection.close()
            case 6:
                elector_running = False

            case _:
                print("Opção inválida!")

        if elector_running:
            input("\nENTER para continuar...")

# =========================
# CANDIDATOS
# =========================

def handle_candidates():
    """
    Controla o fluxo do menu de candidatos.
    """

    candidate_running = True

    while candidate_running:

        choice = candidate_menu()

        match choice:
            case 1:
                list_candidates()
            case 2:

                number = input(
                    "Número "
                    "(0 para voltar): "
                )

                if number != "0":

                    candidate = (
                        get_candidate_by_number(
                            number
                        )
                    )

                    print(
                        candidate
                        if candidate
                        else "Não encontrado!"
                    )
            case 3:

                number = input(
                    "Número "
                    "(0 para voltar): "
                )

                if number != "0":

                    candidate = (
                        get_candidate_by_number(
                            number
                        )
                    )

                    if not candidate:

                        print(
                            "Candidato "
                            "não encontrado!"
                        )

                    else:

                        confirm = input(
                            "Confirma remoção? "
                            "(s/n): "
                        ).lower()

                        if confirm == "s":

                            delete_candidate(number)

                        else:

                            print(
                                "Remoção cancelada."
                            )
            case 4:
                update_candidate()
            case 5:

                name = input(
                    "Nome "
                    "(0 para voltar): "
                )

                if name == "0":
                    continue

                number = input(
                    "Número "
                    "(0 para voltar): "
                )

                if number == "0":
                    continue

                party = input(
                    "Partido "
                    "(0 para voltar): "
                )

                if party == "0":
                    continue

                create_candidate(
                    name,
                    number,
                    party
                )
            case 6:
                candidate_running = False

            case _:
                print("Opção inválida!")

        if candidate_running:
            input("\nENTER para continuar...")


# =========================
# VOTAÇÃO
# =========================

def handle_voting():
    """
    Controla o fluxo do módulo de votação.

    Permite autenticar o mesário, iniciar
    a votação, acessar auditoria e visualizar
    resultados.
    """

    voting_running = True

    while voting_running:

        choice = voting_menu()

        match choice:
            case 1:

                voter_id = input(
                    "Título "
                    "(0 para voltar): "
                )

                if voter_id == "0":
                    continue

                cpf_partial = input(
                    "4 primeiros dígitos "
                    "do CPF "
                    "(0 para voltar): "
                )

                if cpf_partial == "0":
                    continue

                access_key = input(
                    "Chave "
                    "(0 para voltar): "
                )

                if access_key == "0":
                    continue

                if validate_poll_worker(
                    cpf_partial,
                    voter_id,
                    access_key
                ):

                    print("Acesso autorizado!")

                    zeresima()

                    register_opening_log()

                    handle_open_voting()

                else:
                    print("Acesso negado!")
            case 2:
                handle_audit()
            case 3:
                handle_results()
            case 4:
                voting_running = False

            case _:
                print("Opção inválida!")

        if voting_running:
            input("\nENTER para continuar...")

# =========================
# VOTAÇÃO ABERTA
# =========================

def handle_open_voting():
    """
    Controla o fluxo da votação aberta.

    Permite registrar votos e encerrar
    o processo de votação.
    """

    voting_open = True

    while voting_open:

        choice = open_voting_menu()

        match choice:
            case 1:
                cast_vote()
            case 2:

                cpf_partial = input(
                    "4 primeiros dígitos "
                    "do CPF "
                    "(0 para voltar): "
                )

                if cpf_partial == "0":
                    continue

                voter_id = input(
                    "Título do mesário "
                    "(0 para voltar): "
                )

                if voter_id == "0":
                    continue

                access_key = input(
                    "Chave de acesso "
                    "(0 para voltar): "
                )

                if access_key == "0":
                    continue

                if finalize_voting(
                    cpf_partial,
                    voter_id,
                    access_key
                ):
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

    Permite visualizar boletim de urna,
    estatísticas, votos por partido e
    validação de integridade.
    """

    results_running = True

    while results_running:

        choice = results_menu()

        match choice:

            case 1:
                ballot_box()

            case 2:
                statistic_voters()

            case 3:
                elector_choice()

            case 4:
                integrity_validation()
            case 5:
                results_running = False

            case _:
                print("Opção inválida!")

        if results_running:
            input("\nENTER para continuar...")


# =========================
# AUDITORIA
# =========================

def handle_audit():
    """
    Controla o fluxo do módulo de auditoria.

    Permite visualizar logs do sistema
    e protocolos de votação.
    """

    audit_running = True

    while audit_running:

        choice = audit_menu()

        match choice:

            case 1:
                show_logs()

            case 2:
                show_protocols()

            case 3:
                audit_running = False

            case _:
                print("Opção inválida!")

        if audit_running:
            input("\nENTER para continuar...")
