def print_line():
    """
    Exibe uma linha horizontal no terminal para melhorar a organização visual.
    """
    print("-" * 50)

def show_menu(title, options):
    """
    Exibe um menu dinâmico com base em um título e uma lista de opções.

    Args:
        title (str): Título do menu.
        options (list): Lista de opções que serão exibidas.

    Returns:
        int: Opção selecionada pelo usuário.
        None: Caso a entrada seja inválida.
    """
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
        print("\n Entrada inválida! Tente novamente.")


def main_menu():
    """
    Exibe o menu principal do sistema.

    Returns:
        int: Opção escolhida pelo usuário no menu principal.
    """
    return show_menu("MENU", ["GERENCIAMENTO", "VOTAÇÃO", "RESULTADOS", "AUDITORIA", "ENCERRAR"])


def management_menu():
    """
    Exibe o menu de gerenciamento do sistema.

    Returns:
        int: Opção escolhida (Eleitores ou Candidatos).
    """
    return show_menu("GERENCIAMENTO", ["ELEITORES", "CANDIDATOS", "VOLTAR"])


def results_menu():
    """
    Exibe o menu de resultados da votação.

    Returns:
        int: Opção escolhida para visualização dos resultados.
    """
    return show_menu(
        "RESULTADOS",
        [
            "BOLETIM DE URNA",
            "ESTATÍSTICAS",
            "VOTOS POR PARTIDO",
            "VALIDAÇÃO DE INTEGRIDADE",
            "VOLTAR",
        ],
    )


def audit_menu():
    """
    Exibe o menu de auditoria do sistema.

    Returns:
        int: Opção escolhida para auditoria (logs ou protocolos).
    """
    return show_menu("AUDITORIA", ["LOGS DO SISTEMA", "PROTOCOLOS", "VOLTAR"])


def elector_menu():
    """
    Exibe o menu de gerenciamento de eleitores.

    Returns:
        int: Opção escolhida para operações com eleitores.
    """
    return show_menu(
        "ELEITORES",
        [
            "LISTAR ELEITORES",
            "BUSCAR ELEITORES",
            "REMOVER ELEITORES",
            "EDITAR DADOS",
            "CADASTRAR ELEITORES",
            "VOLTAR",
        ],
    )


def candidate_menu():
    """
    Exibe o menu de gerenciamento de candidatos.

    Returns:
        int: Opção escolhida para operações com candidatos.
    """
    return show_menu(
        "CANDIDATOS",
        [
            "LISTAR CANDIDATOS",
            "BUSCAR CANDIDATOS",
            "REMOVER CANDIDATOS",
            "EDITAR DADOS",
            "CADASTRAR CANDIDATOS",
            "VOLTAR",
        ],
    )