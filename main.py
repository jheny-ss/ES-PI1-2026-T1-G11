def print_line():
    """
    Prints a horizontal separator line to improve menu visualization.
    """
    print("-" * 50)


def show_main_menu():
    """
    Displays the main system menu with all available options.
    """
    print_line()
    print("MENU".center(50))
    print_line()
    print("\n1 - GERENCIAMENTO")
    print("2 - VOTAÇÃO")
    print("3 - RESULTADOS")
    print("4 - AUDITORIA")


def management_menu():
    """
    Displays the management menu and handles user selection
    between voters and candidates.
    """
    print_line()
    print("\n" + "GERENCIAMENTO".center(50, "-"))
    print("\n1 - ELEITORES")
    print("2 - CANDIDATOS")

    management_option = int(input("\nQUEM VOCÊ DESEJA GERENCIAR: "))
    print_line()

    match management_option:
        case 1:
            print("\n" + "ELEITORES".center(50, "-"))
        case 2:
            print("\n" + "CANDIDATOS".center(50, "-"))


def voting_menu():
    """
    Displays the voting menu and processes actions such as
    opening the system, voting, or closing the voting process.
    """
    print_line()
    print("\n" + "VOTAÇÃO".center(50, "-"))
    print("\n1 - ABRIR SISTEMA")
    print("2 - VOTAR")
    print("3 - ENCERRAR VOTAÇÃO")

    voting_option = int(input("\nO QUE VOCÊ DESEJA FAZER: "))
    print_line()

    match voting_option:
        case 1:
            print("\n" + "ABRIR SISTEMA".center(50, "-"))
        case 2:
            print("\n" + "VOTAR".center(50, "-"))
        case 3:
            print("\n" + "ENCERRAR VOTAÇÃO".center(50, "-"))


def results_menu():
    """
    Displays the results menu and allows the user to select
    different types of reports and statistics.
    """
    print_line()
    print("\n" + "RESULTADOS".center(50, "-"))
    print("\n1 - BOLETIM DE URNA")
    print("2 - ESTATÍSTICAS")
    print("3 - VOTOS POR PARTIDO")
    print("4 - VALIDAÇÃO DE INTEGRIDADE")

    results_option = int(input("\nO QUE VOCÊ DESEJA VISUALIZAR: "))
    print_line()

    match results_option:
        case 1:
            print("\n" + "BOLETIM DE URNA".center(50, "-"))
        case 2:
            print("\n" + "ESTATÍSTICAS".center(50, "-"))
        case 3:
            print("\n" + "VOTOS POR PARTIDO".center(50, "-"))
        case 4:
            print("\n" + "VALIDAÇÃO DE INTEGRIDADE".center(50, "-"))


def audit_menu():
    """
    Displays the audit menu and provides access to system logs
    and voting protocols.
    """
    print_line()
    print("\n" + "AUDITORIA".center(50, "-"))
    print("\n1 - LOGS DO SISTEMA")
    print("2 - PROTOCOLOS DE VOTAÇÃO")

    audit_option = int(input("\nO QUE VOCÊ DESEJA VISUALIZAR: "))
    print_line()

    match audit_option:
        case 1:
            print("\n" + "LOGS DO SISTEMA".center(50, "-"))
        case 2:
            print("\n" + "PROTOCOLOS DE VOTAÇÃO".center(50, "-"))


# MAIN PROGRAM
"""
Main execution block of the voting system.
Displays the main menu and routes the user
to the selected module.
"""
show_main_menu()
main_menu_option = int(input("\nSELECIONE UMA OPÇÃO: "))

match main_menu_option:
    case 1:
        management_menu()
    case 2:
        voting_menu()
    case 3:
        results_menu()
    case 4:
        audit_menu()