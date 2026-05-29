from database.connection import get_cursor

from models.crypto.decrypt import decrypt_hill_cipher
from models.crypto.encrypt import encrypt_hill_cipher

from models.audit import (
    register_management_log,
    register_error_log
)


def list_electors():
    """
    Lista todos os eleitores cadastrados no sistema. 
    Os dados criptografados são descriptografados antes da exibição.
    
    Args: 
        None 
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

        dados = []

        for elector in electors:

            dados.append({
                "id":            str(elector["id"]),
                "nome":          elector["nome"],
                "cpf":           decrypt_hill_cipher(elector["cpf"]),
                "titulo":        decrypt_hill_cipher(elector["titulo_eleitor"]),
                "chave":         decrypt_hill_cipher(elector["chave_acesso"]),
                "mesario":       "Sim" if elector["status_mesario"] else "Não",
            })

        maior_id      = max(len(e["id"])      for e in dados)
        maior_nome    = max(len(e["nome"])    for e in dados)
        maior_cpf     = max(len(e["cpf"])     for e in dados)
        maior_titulo  = max(len(e["titulo"])  for e in dados)
        maior_chave   = max(len(e["chave"])   for e in dados)
        maior_mesario = max(len(e["mesario"]) for e in dados)

        maior_id      = max(maior_id,      len("ID"))
        maior_nome    = max(maior_nome,    len("Nome"))
        maior_cpf     = max(maior_cpf,     len("CPF"))
        maior_titulo  = max(maior_titulo,  len("Título"))
        maior_chave   = max(maior_chave,   len("Chave"))
        maior_mesario = max(maior_mesario, len("Mesário"))

        margem = " " * 2

        cabecalho = (
            f"{margem}{'ID':<{maior_id}}  "
            f"{'Nome':<{maior_nome}}  "
            f"{'CPF':<{maior_cpf}}  "
            f"{'Título':<{maior_titulo}}  "
            f"{'Chave':<{maior_chave}}  "
            f"{'Mesário':<{maior_mesario}}"
        )

        separador = (
            f"{margem}{'─'*maior_id}  "
            f"{'─'*maior_nome}  "
            f"{'─'*maior_cpf}  "
            f"{'─'*maior_titulo}  "
            f"{'─'*maior_chave}  "
            f"{'─'*maior_mesario}"
        )

        print(cabecalho)
        print(separador)

        for e in dados:

            print(
                f"{margem}{e['id']:<{maior_id}}  "
                f"{e['nome']:<{maior_nome}}  "
                f"{e['cpf']:<{maior_cpf}}  "
                f"{e['titulo']:<{maior_titulo}}  "
                f"{e['chave']:<{maior_chave}}  "
                f"{e['mesario']:<{maior_mesario}}"
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
    Busca um eleitor pelo CPF. 

    Args: 
        cpf (str): CPF do eleitor. 

    Returns: 
        dict | None: Dicionário contendo os dados do eleitor encontrado ou None caso não exista.
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

def print_elector(elector: dict):    
    """ 
    Exibe os dados de um eleitor formatados no terminal. 

    Args: 
    elector (dict): Dicionário contendo os dados do eleitor. 

    Returns: 
        None 
    """  
    campos = [
        ("ID",           str(elector["id"])),
        ("Nome",         elector["nome"]),
        ("CPF",          elector["cpf"]),
        ("Título",       elector["titulo_eleitor"]),
        ("Chave",        elector["chave_acesso"]),
        ("Votou",        "Sim" if elector["status_votacao"] else "Não"),
        ("Mesário",      "Sim" if elector["status_mesario"] else "Não"),
     ]

    maior_chave = max(len(c[0]) for c in campos)
    maior_valor = max(len(c[1]) for c in campos)
    largura     = maior_chave + maior_valor + 5

    linhas = [
        f"{'\n===== ELEITOR =====':^{largura}}",
    ]

    for chave, valor in campos:
        conteudo = f"  {chave:<{maior_chave}}  {valor:<{maior_valor}}  "
        linhas.append(f"{conteudo}")


    print("\n".join(linhas))


def create_elector(
    cursor,
    name,
    cpf,
    voter_id,
    access_key,
    is_poll_worker
):
    """
    Cadastra um novo eleitor no banco de dados. 
    
    Args: 
        cursor (Cursor): Cursor utilizado para executar comandos SQL. 
        name (str): Nome do eleitor. 
        cpf (str): CPF do eleitor. 
        voter_id (str): Título de eleitor. 
        access_key (str): Chave de acesso do eleitor. 
        is_poll_worker (bool): Indica se o eleitor possui função de mesário. 
       
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
    Remove um eleitor do sistema utilizando o CPF.

    Args: 
        cpf (str): CPF do eleitor. 

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
    Atualiza os dados de um eleitor cadastrado. 

    Args: 
        cpf (str): CPF do eleitor. 
        name (str): Novo nome do eleitor. 
        voter_id (str): Novo título de eleitor. 
        is_poll_worker (bool): Novo status de mesário. 

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
    Verifica se já existe um eleitor cadastrado com o CPF ou título de eleitor informados. 
    
    Args: 
    cursor (Cursor): Cursor utilizado para executar comandos SQL. 
        cpf (str): CPF do eleitor. 
        voter_id (str): Título de eleitor. 

    Returns: 
        bool: True se o eleitor já estiver cadastrado. False caso contrário.
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
