from models.elector import (
    listar_eleitores,
    buscar_eleitor,
    remover_eleitor,
    editar_eleitor,
    inserir_eleitor
)

from models.candidate import (
    listar_candidatos,
    buscar_candidato,
    remover_candidato,
    editar_candidato,
    inserir_candidato
)

from views.menus import (
    main_menu,
    management_menu,
    voting_menu,
    results_menu,
    audit_menu,
    elector_menu,
    candidate_menu,
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
              handle_audit()
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
            return handle_electors()
        case 2:
            return handle_candidates()
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

def handle_audit():
    """
    Controla o fluxo do módulo de auditoria.
    """
    choice = audit_menu()

    match choice:
        case 1:
            print("Logs do sistema...")
            input("\nPressione ENTER para continuar...")
            return handle_audit()

        case 2:
            print("Protocolos...")
            input("\nPressione ENTER para continuar...")
            return handle_audit()

        case 3: # VOLTAR
            return

        case _:
            print("Opção inválida!")
            input("\nPressione ENTER para continuar...")
            return handle_audit()

def handle_electors():
    """
    Controla o fluxo do menu de eleitores.
    """
    choice = elector_menu()

    match choice:
        case 1:
          listar_eleitores()

          input("\nPressione ENTER para continuar...")
          return handle_electors()

        case 2:
          cpf = input("Digite o CPF: ")
          eleitor = buscar_eleitor(cpf)

          if eleitor:
            print("\nELEITOR ENCONTRADO:")
            print(eleitor)
          else:
            print("Eleitor não encontrado!")

          input("\nPressione ENTER para continuar...")
          return handle_electors()

        case 3:
          cpf = input("CPF do eleitor a remover: ")
          remover_eleitor(cpf)

          input("\nPressione ENTER para continuar...")
          return handle_electors()

        case 4:
          editar_eleitor()

          input("\nPressione ENTER para continuar...")
          return handle_electors()

        case 5:
          nome = input("Nome: ")
          cpf = input("CPF: ")
          titulo = input("Título: ")
          chave = input("Chave: ")

          inserir_eleitor(nome, cpf, titulo, chave)

          input("\nPressione ENTER para continuar...")
          return handle_electors()

        case 6:  # VOLTAR
          return handle_management()

        case _:
          print("Opção inválida!")
          input("\nPressione ENTER para continuar...")
          return handle_electors()

def handle_candidates():
    """
    Controla o fluxo do menu de candidatos.
    """
    choice = candidate_menu()

    match choice:
        case 1:
          listar_candidatos()

          input("\nPressione ENTER para continuar...")
          return handle_candidates()
        case 2:
          numero = input("Número do candidato: ")
          candidato = buscar_candidato(numero)

          if candidato:
            print("\nCANDIDATO ENCONTRADO:")
            print(candidato)
          else:
            print("Candidato não encontrado!")

          input("\nPressione ENTER para continuar...")
          return handle_candidates()
        case 3:
          numero = input("Número do candidato a remover: ")
          remover_candidato(numero)

          input("\nPressione ENTER para continuar...")
          return handle_candidates()
        case 4:

          editar_candidato()

          input("\nPressione ENTER para continuar...")
          return handle_candidates()
        case 5:
          nome = input("Nome: ")
          numero = input("Número: ")
          partido = input("Partido: ")

          inserir_candidato(nome, numero, partido)

          input("\nPressione ENTER para continuar...")
          return handle_candidates()
        case 6:  # VOLTAR
          return handle_management()
        case _:
          print("Opção inválida!")
          input("\nPressione ENTER para continuar...")
          return handle_candidates()
