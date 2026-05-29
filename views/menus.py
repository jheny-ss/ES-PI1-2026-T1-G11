import os


def print_line():
    """
    Exibe uma linha horizontal de separação no terminal.

    Args:
        None

    Returns:
        None:
            Não retorna valor.
    """
    print("-" * 50)


def clear_terminal():
    """
    Limpa a tela do terminal de acordo com o sistema operacional.

    Args:
        None

    Returns:
        None:
            Não retorna valor.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def show_menu(title, options):
    """
    Exibe um menu de opções e retorna a escolha do usuário.

    Args:
        title (str):
            Título do menu.

        options (list):
            Lista contendo as opções a serem exibidas.

    Returns:
        int:
            Retorna o número da opção selecionada pelo usuário.
            Retorna -1 caso seja informado um valor inválido.
    """
    clear_terminal()
    print_line()
    print(title.center(50))
    print_line()

    for i, option in enumerate(options, start=1):
        print(f"{i} - {option}")

    try:
        choice = int(input("\nSELECIONE UMA OPÇÃO: "))
        print_line()
        return choice
    except ValueError:
        print("\nEntrada inválida!")
        return -1


def main_menu():
    """
    Exibe o menu principal do sistema.

    Args:
        None

    Returns:
        int:
            Opção selecionada pelo usuário.
    """
    return show_menu("MENU", ["GERENCIAMENTO", "VOTAÇÃO", "SAIR"])


def management_menu():
    """
    Exibe o menu de gerenciamento.

    Args:
        None

    Returns:
        int:
            Opção selecionada pelo usuário.
    """
    return show_menu("GERENCIAMENTO", ["ELEITORES", "CANDIDATOS", "VOLTAR"])


def voting_menu():
    """
    Exibe o menu principal da votação.

    Args:
        None

    Returns:
        int:
            Opção selecionada pelo usuário.
    """
    return show_menu("VOTAÇÃO", [
        "ABRIR SISTEMA DE VOTAÇÃO",
        "AUDITORIA",
        "RESULTADOS",
        "VOLTAR"
    ])


def open_voting_menu():
    """
    Exibe o menu disponível durante o período de votação aberta.

    Args:
        None

    Returns:
        int:
            Opção selecionada pelo usuário.
    """
    return show_menu("VOTAÇÃO ABERTA", [
        "VOTAR",
        "ENCERRAR VOTAÇÃO",
        "VOLTAR"
    ])


def results_menu():
    """
    Exibe o menu de resultados da eleição.

    Args:
        None

    Returns:
        int:
            Opção selecionada pelo usuário.
    """
    return show_menu("RESULTADOS", [
        "BOLETIM DE URNA",
        "ESTATÍSTICAS",
        "VOTOS POR PARTIDO",
        "VALIDAÇÃO DE INTEGRIDADE",
        "VOLTAR"
    ])


def audit_menu():
    """
    Exibe o menu de auditoria do sistema.

    Args:
        None

    Returns:
        int:
            Opção selecionada pelo usuário.
    """
    return show_menu("AUDITORIA", [
        "LOGS DO SISTEMA",
        "PROTOCOLOS",
        "VOLTAR"
    ])


def elector_menu():
    """
    Exibe o menu de gerenciamento de eleitores.

    Args:
        None

    Returns:
        int:
            Opção selecionada pelo usuário.
    """
    return show_menu("ELEITORES", [
        "LISTAR ELEITORES",
        "BUSCAR ELEITOR",
        "REMOVER ELEITOR",
        "EDITAR DADOS",
        "CADASTRAR ELEITOR",
        "VOLTAR"
    ])


def candidate_menu():
    """
    Exibe o menu de gerenciamento de candidatos.

    Args:
        None

    Returns:
        int:
            Opção selecionada pelo usuário.
    """
    return show_menu("CANDIDATOS", [
        "LISTAR CANDIDATOS",
        "BUSCAR CANDIDATO",
        "REMOVER CANDIDATO",
        "EDITAR DADOS",
        "CADASTRAR CANDIDATO",
        "VOLTAR"
    ])