from database.connection import get_cursor

from models.audit import (
    register_management_log,
    register_error_log
)


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

        for candidate in candidates:

            print(
                f"{candidate['nome']} - "
                f"{candidate['numero_de_votacao']} - "
                f"{candidate['partido']}"
            )

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
