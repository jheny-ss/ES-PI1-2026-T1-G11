from database.connection import get_cursor

from models.audit import (
    register_management_log,
    register_error_log
)

def validate_candidate_number(number):
    """
    Valida número de candidato.

    Regras:
    - Deve conter apenas números
    - Deve ter entre 2 e 5 dígitos
    """

    number = number.strip()

    # Apenas números
    if not number.isdigit():
        return False

    # Tamanho permitido
    if len(number) < 2 or len(number) > 5:
        return False

    return True


def list_candidates():
    """
    Lista todos os candidatos cadastrados.

    Returns:
        None
    """

    connection, cursor = get_cursor()

    try:

        cursor.execute(
            """
            SELECT *
            FROM candidatos
            """
        )

        candidates = cursor.fetchall()

        print("\n===== LISTA DE CANDIDATOS =====\n")

        if not candidates:
            print("Nenhum candidato cadastrado!")
            return

        maior_nome    = max(len(c["nome"])                    for c in candidates)
        maior_numero  = max(len(str(c["numero_de_votacao"]))  for c in candidates)
        maior_partido = max(len(c["partido"])                 for c in candidates)

        maior_nome    = max(maior_nome,    len("Nome"))
        maior_numero  = max(maior_numero,  len("Número"))
        maior_partido = max(maior_partido, len("Partido"))

        margem = " " * 2  

        cabecalho = f"{margem}{'Nome':<{maior_nome}}  {'Número':>{maior_numero}}  {'Partido':<{maior_partido}}"
        separador = f"{margem}{'─'*maior_nome}  {'─'*maior_numero}  {'─'*maior_partido}"

        print(cabecalho)
        print(separador)

        for candidate in candidates:
            linha = (
                f"{margem}{candidate['nome']:<{maior_nome}}  "
                f"{str(candidate['numero_de_votacao']):>{maior_numero}}  "
                f"{candidate['partido']:<{maior_partido}}"
            )
            print(linha)

    except Exception as error:

        register_error_log(error)

        print(
            "Erro ao listar candidatos!"
        )

    finally:

        cursor.close()
        connection.close()


def get_candidate_by_number(number):
    """
    Busca candidato pelo número.

    Args:
        number (str):
            Número do candidato.

    Returns:
        dict | None
    """

    connection, cursor = get_cursor()

    try:

        cursor.execute(
            """
            SELECT *
            FROM candidatos
            WHERE numero_de_votacao = %s
            """,
            (number,)
        )

        return cursor.fetchone()

    except Exception as error:

        register_error_log(error)

        return None

    finally:

        cursor.close()
        connection.close()

def print_candidate(candidate: dict):      
    campos = [
        ("ID",           str(candidate["id"])),
        ("Nome",         candidate["nome"]),
        ("Número",       str(candidate["numero_de_votacao"])),
        ("Partido",      candidate["partido"]),
    ]

    maior_chave = max(len(c[0]) for c in campos)
    maior_valor = max(len(c[1]) for c in campos)
    largura     = maior_chave + maior_valor + 5

    linhas = [
        f"{'\n===== CANDIDATO =====':^{largura}}",
    ]

    for chave, valor in campos:
        conteudo = f"  {chave:<{maior_chave}}  {valor:<{maior_valor}}  "
        linhas.append(f"{conteudo}")


    print("\n".join(linhas))


def create_candidate(name, number, party):
    """
    Cadastra um novo candidato.

    Args:
        name (str):
            Nome do candidato.

        number (str):
            Número eleitoral.

        party (str):
            Partido político.

    Returns:
        None
    """

    if not validate_candidate_number(number):
        print("Número inválido!")
        return

    connection, cursor = get_cursor()

    try:

        cursor.execute(
            """
            SELECT id
            FROM candidatos
            WHERE numero_de_votacao = %s
            """,
            (number,)
        )

        result = cursor.fetchone()

        if result is not None:

            print(
                "Número de candidato já existe!"
            )

            return

        cursor.execute(
            """
            INSERT INTO candidatos
            (
                nome,
                numero_de_votacao,
                partido
            )
            VALUES (%s, %s, %s)
            """,
            (name, number, party)
        )

        connection.commit()

        print(
            "Candidato cadastrado!"
        )

        register_management_log(
            "Cadastro de candidato",
            name
        )

    except Exception as error:

        connection.rollback()

        register_error_log(error)

        print(
            "Erro ao cadastrar candidato!"
        )

    finally:

        cursor.close()
        connection.close()


def delete_candidate(number):
    """
    Remove candidato pelo número.

    Args:
        number (str):
            Número do candidato.

    Returns:
        None
    """

    connection, cursor = get_cursor()

    try:

        cursor.execute(
            """
            DELETE FROM candidatos
            WHERE numero_de_votacao = %s
            """,
            (number,)
        )

        connection.commit()

        if cursor.rowcount > 0:

            print(
                "Candidato removido!"
            )

            register_management_log(
                "Remoção de candidato",
                number
            )

        else:

            print(
                "Candidato não encontrado!"
            )

    except Exception as error:

        connection.rollback()

        register_error_log(error)

        print(
            "Erro ao remover candidato!"
        )

    finally:

        cursor.close()
        connection.close()


def update_candidate():
    """
    Atualiza dados de um candidato.

    Returns:
        None
    """

    connection, cursor = get_cursor()

    try:

        found = False

        while not found:

            number = input(
                "Número do candidato: "
            )

            cursor.execute(
                """
                SELECT id
                FROM candidatos
                WHERE numero_de_votacao = %s
                """,
                (number,)
            )

            result = cursor.fetchone()

            if result:

                found = True

            else:

                print(
                    "Candidato não encontrado!"
                )

        name = input("Novo nome: ")
        party = input("Novo partido: ")

        cursor.execute(
            """
            UPDATE candidatos
            SET nome = %s,
                partido = %s
            WHERE numero_de_votacao = %s
            """,
            (name, party, number)
        )

        connection.commit()

        print(
            "Candidato atualizado!"
        )

        register_management_log(
            "Atualização de candidato",
            number
        )

    except Exception as error:

        connection.rollback()

        register_error_log(error)

        print(
            "Erro ao atualizar candidato!"
        )

    finally:

        cursor.close()
        connection.close()


def validate_candidate_number(number):
    """
    Valida número de candidato.

    Regras:
    - Deve conter apenas números
    - Deve ter entre 2 e 5 dígitos
    """

    number = number.strip()

    # Apenas números
    if not number.isdigit():
        return False

    # Tamanho permitido
    if len(number) < 2 or len(number) > 5:
        return False

    return True