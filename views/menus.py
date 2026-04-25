def print_line():
    print("-" * 50)


def show_menu(title, options):
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
    return show_menu("MENU", ["GERENCIAMENTO", "VOTAÇÃO", "SAIR"])


def management_menu():
    return show_menu("GERENCIAMENTO", ["ELEITORES", "CANDIDATOS", "VOLTAR"])


def voting_menu():
    return show_menu("VOTAÇÃO", [
        "ABRIR SISTEMA DE VOTAÇÃO",
        "AUDITORIA",
        "RESULTADOS",
        "VOLTAR"
    ])


def open_voting_menu():
    return show_menu("VOTAÇÃO ABERTA", [
        "VOTAR",
        "ENCERRAR VOTAÇÃO",
        "VOLTAR"
    ])


def results_menu():
    return show_menu("RESULTADOS", [
        "BOLETIM DE URNA",
        "ESTATÍSTICAS",
        "VOTOS POR PARTIDO",
        "VALIDAÇÃO DE INTEGRIDADE",
        "VOLTAR"
    ])


def audit_menu():
    return show_menu("AUDITORIA", [
        "LOGS DO SISTEMA",
        "PROTOCOLOS",
        "VOLTAR"
    ])


def elector_menu():
    return show_menu("ELEITORES", [
        "LISTAR ELEITORES",
        "BUSCAR ELEITOR",
        "REMOVER ELEITOR",
        "EDITAR DADOS",
        "CADASTRAR ELEITOR",
        "VOLTAR"
    ])


def candidate_menu():
    return show_menu("CANDIDATOS", [
        "LISTAR CANDIDATOS",
        "BUSCAR CANDIDATO",
        "REMOVER CANDIDATO",
        "EDITAR DADOS",
        "CADASTRAR CANDIDATO",
        "VOLTAR"
    ])