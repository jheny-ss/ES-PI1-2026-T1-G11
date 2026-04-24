from views.menus import (
    main_menu,
    management_menu,
    voting_menu,
    results_menu,
)

def run_system():
    """
    Controla o fluxo principal do sistema.

    Exibe continuamente o menu principal e direciona o usuário
    para o módulo selecionado.
    """

    choice = main_menu()

    match choice:
          case 1:
              handle_management()
              return True
          case 2:
              handle_voting()
              return True
          case 3:
              handle_results()
              return True
          case 4:
            print("\nAbrindo sistema de auditoria...")
            input("\nPressione ENTER para continuar...")
            return True
          case 5:
            print("\nEncerrando sistema...")
            return False
          case _:
              print("Opção inválida!")
              return True

def handle_management():
    """
    Controla o fluxo do módulo de gerenciamento.

    Direciona o usuário para o gerenciamento de eleitores ou candidatos.
    """
    choice = management_menu()

    match choice:
        case 1:
            print("\nGerenciamento de eleitores...")
            input("\nPressione ENTER para continuar...")
        case 2:
            print("\nGerenciamento de candidatos...")
            input("\nPressione ENTER para continuar...")
        case 3: #VOLTAR
            return
        case _:
            print("Opção inválida!")
            return handle_management()

def handle_voting():
    """
    Controla o fluxo do módulo de votação.
    """
    choice = voting_menu()

    match choice:
        case 1:
            print("Abrindo sistema de votação...")
            input("\nPressione ENTER para continuar...")
            return handle_voting()

        case 2:
            print("Votar...")
            input("\nPressione ENTER para continuar...")
            return handle_voting()

        case 3:
            print("Encerrando votação...")
            input("\nPressione ENTER para continuar...")
            return handle_voting()

        case 4:  # VOLTAR
            return

        case _:
            print("Opção inválida!")
            input("\nPressione ENTER para continuar...")
            return handle_voting()

def handle_results():
    """
    Controla o fluxo do módulo de resultados.
    """
    choice = results_menu()

    match choice:
        case 1:
            print("Boletim de urna...")
            input("\nPressione ENTER para continuar...")
            return handle_results()

        case 2:
            print("Estatísticas...")
            input("\nPressione ENTER para continuar...")
            return handle_results()

        case 3:
            print("Votos por Partido...")
            input("\nPressione ENTER para continuar...")
            return handle_results()

        case 4:
            print("Validação de Integridade...")
            input("\nPressione ENTER para continuar...")
            return handle_results()

        case 5:  # VOLTAR
            return

        case _:
            print("Opção inválida!")
            input("\nPressione ENTER para continuar...")
            return handle_voting()
        