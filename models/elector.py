from database.connection import get_cursor

from models.crypto.decrypt import decrypt_hill_cipher
from models.crypto.encrypt import encrypt_hill_cipher

from models.audit import (
    register_management_log,
    register_error_log
)


def list_electors():
    """
    Lista todos os eleitores.

    Returns:
        None
    """

    connection, cursor = get_cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                nome,
                cpf,
                titulo_eleitor,
                chave_acesso,
                status_mesario
            FROM eleitores
            """
        )

        electors = cursor.fetchall()

        print(
            "\n===== LISTA DE ELEITORES =====\n"
        )

        if not electors:

            print(
                "Nenhum eleitor cadastrado!"
            )

            return

        for elector in electors:

            decrypted_cpf = decrypt_hill_cipher(
                elector["cpf"]
            )

            decrypted_voter_id = decrypt_hill_cipher(
                elector["titulo_eleitor"]
            )

            decrypted_key = decrypt_hill_cipher(
                elector["chave_acesso"]
            )

            print(
                f"{elector['id']} - "
                f"{elector['nome']} - "
                f"{decrypted_cpf} - "
                f"{decrypted_voter_id} - "
                f"{decrypted_key} - "
                f"Mesário: {elector['status_mesario']}"
            )

    except Exception as error:

        register_error_log(error)

        print(
            "Erro ao listar eleitores!"
        )

    finally:

        cursor.close()
        connection.close()


def get_elector_by_cpf(cpf):
    """
    Busca eleitor pelo CPF.

    Args:
        cpf (str):
            CPF do eleitor.

    Returns:
        dict | None
    """

    connection, cursor = get_cursor()

    try:

        encrypted_cpf = encrypt_hill_cipher(
            cpf
        )

        cursor.execute(
            """
            SELECT *
            FROM eleitores
            WHERE cpf = %s
            """,
            (encrypted_cpf,)
        )

        elector = cursor.fetchone()

        if elector:

            elector["cpf"] = decrypt_hill_cipher(
                elector["cpf"]
            )

            elector["titulo_eleitor"] = (
                decrypt_hill_cipher(
                    elector["titulo_eleitor"]
                )
            )

            elector["chave_acesso"] = (
                decrypt_hill_cipher(
                    elector["chave_acesso"]
                )
            )

        return elector

    except Exception as error:

        register_error_log(error)

        print("Erro ao buscar eleitor!")

        return None

    finally:

        cursor.close()
        connection.close()


def create_elector(
    cursor,
    name,
    cpf,
    voter_id,
    access_key,
    is_poll_worker
):
    """
    Cadastra eleitor.

    Args:
        cursor:
            Cursor do banco.

        name (str):
            Nome do eleitor.

        cpf (str):
            CPF do eleitor.

        voter_id (str):
            Título eleitoral.

        access_key (str):
            Chave de acesso.

        is_poll_worker (bool):
            Status de mesário.

    Returns:
        None
    """

    encrypted_cpf = encrypt_hill_cipher(
        cpf
    )

    encrypted_voter_id = encrypt_hill_cipher(
        voter_id
    )

    encrypted_key = encrypt_hill_cipher(
        access_key
    )

    cursor.execute(
        """
        INSERT INTO eleitores
        (
            nome,
            cpf,
            titulo_eleitor,
            chave_acesso,
            status_mesario
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            name,
            encrypted_cpf,
            encrypted_voter_id,
            encrypted_key,
            is_poll_worker
        )
    )

    register_management_log(
        "Cadastro de eleitor",
        name
    )


def delete_elector(cpf):
    """
    Remove eleitor pelo CPF.

    Args:
        cpf (str):
            CPF do eleitor.

    Returns:
        None
    """

    connection, cursor = get_cursor()

    try:

        encrypted_cpf = encrypt_hill_cipher(
            cpf
        )

        cursor.execute(
            """
            DELETE FROM eleitores
            WHERE cpf = %s
            """,
            (encrypted_cpf,)
        )

        connection.commit()

        if cursor.rowcount > 0:

            print(
                "Eleitor removido!"
            )

            register_management_log(
                "Remoção de eleitor",
                cpf
            )

        else:

            print(
                "Eleitor não encontrado!"
            )

    except Exception as error:

        connection.rollback()

        register_error_log(error)

        print(
            "Erro ao remover eleitor!"
        )

    finally:

        cursor.close()
        connection.close()


def update_elector_db(
    cpf,
    name,
    voter_id,
    is_poll_worker
):
    """
    Atualiza dados do eleitor.

    Args:
        cpf (str):
            CPF do eleitor.

        name (str):
            Novo nome.

        voter_id (str):
            Novo título.

        is_poll_worker (bool):
            Novo status de mesário.

    Returns:
        None
    """

    connection, cursor = get_cursor()

    try:

        encrypted_cpf = encrypt_hill_cipher(
            cpf
        )

        encrypted_voter_id = encrypt_hill_cipher(
            voter_id
        )

        cursor.execute(
            """
            UPDATE eleitores
            SET
                nome = %s,
                titulo_eleitor = %s,
                status_mesario = %s
            WHERE cpf = %s
            """,
            (
                name,
                encrypted_voter_id,
                is_poll_worker,
                encrypted_cpf
            )
        )

        connection.commit()

        register_management_log(
            "Atualização de eleitor",
            cpf
        )

        print(
            "Eleitor atualizado!"
        )

    except Exception as error:

        connection.rollback()

        register_error_log(error)

        print(
            "Erro ao atualizar eleitor!"
        )

    finally:

        cursor.close()
        connection.close()


def elector_exists(cursor, cpf, voter_id):
    """
    Verifica se eleitor já existe.

    Args:
        cursor:
            Cursor do banco.

        cpf (str):
            CPF do eleitor.

        voter_id (str):
            Título eleitoral.

    Returns:
        bool
    """

    encrypted_cpf = encrypt_hill_cipher(
        cpf
    )

    encrypted_voter_id = encrypt_hill_cipher(
        voter_id
    )

    cursor.execute(
        """
        SELECT 1
        FROM eleitores
        WHERE cpf = %s
        OR titulo_eleitor = %s
        """,
        (
            encrypted_cpf,
            encrypted_voter_id
        )
    )

    return cursor.fetchone() is not None
