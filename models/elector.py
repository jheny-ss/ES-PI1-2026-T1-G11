from database.connection import get_cursor
from models.voting import generate_access_key


def list_electors():
    """
    Lista todos os eleitores.
    """
    connection, cursor = get_cursor()

    cursor.execute("SELECT id, nome, titulo_eleitor, chave_acesso, status_mesario FROM eleitores")

    print("\nLISTA DE ELEITORES:")

    for elector in cursor.fetchall():
        print(f"{elector['id']} - {elector['nome']} - {elector['titulo_eleitor']} - {elector['chave_acesso']} - {elector['status_mesario']}")

    cursor.close()
    connection.close()


def get_elector_by_cpf(cpf):
    """
    Busca eleitor pelo CPF.
    """
    connection, cursor = get_cursor()

    cursor.execute("SELECT * FROM eleitores WHERE cpf = %s", (cpf,))
    elector = cursor.fetchone()

    cursor.close()
    connection.close()

    return elector


def create_elector(name, cpf, voter_id, access_key, is_poll_worker):
    """
    Cadastra um novo eleitor.
    """
    connection, cursor = get_cursor()

    sql = """
        INSERT INTO eleitores (nome, cpf, titulo_eleitor,chave_acesso,status_mesario)
        VALUES (%s, %s, %s,%s,%s)
    """

    cursor.execute(sql, (name, cpf, voter_id, access_key, is_poll_worker))
    connection.commit()

    print("Eleitor cadastrado!")

    cursor.close()
    connection.close()


def delete_elector(cpf):
    """
    Remove eleitor pelo CPF.
    """
    connection, cursor = get_cursor()

    cursor.execute("DELETE FROM eleitores WHERE cpf = %s", (cpf,))
    connection.commit()

    print("Eleitor removido!")

    cursor.close()
    connection.close()


def update_elector():
    """
    Edita eleitor pelo CPF.
    """
    cpf = input("CPF do eleitor: ")

    connection, cursor = get_cursor()
    cursor.execute("SELECT id FROM eleitores WHERE cpf = %s", (cpf,))
    result = cursor.fetchone()

    if result is None:
        print("Eleitor não encontrado!")
        cursor.close()
        connection.close()
        return

    # Só pede os dados se o eleitor existir
    name   = input("Novo nome: ")
    voter_id = input("Novo título: ")
    access_key  = input("Nova chave: ")

    is_poll_worker_input = ""
    while is_poll_worker_input != "Sim" and is_poll_worker_input != "Não":
        is_poll_worker_input = input("Status de Mesário (Sim/Não): ")
        if is_poll_worker_input not in ["Sim", "Não"]:
            print("Status inválido!")
            input("\nPressione ENTER para corrigir...")
        else:
            if is_poll_worker_input == "Sim":
                is_poll_worker = True
            else:
                is_poll_worker = False

    cursor.execute(
    "UPDATE eleitores SET nome = %s, titulo_eleitor = %s, chave_acesso = %s, status_mesario = %s WHERE cpf = %s",
    (name, voter_id, access_key, is_poll_worker, cpf)
    )
    connection.commit()

    print("Eleitor atualizado com sucesso!")
    cursor.close()
    connection.close()

def elector_exists(cpf, voter_id):
    connection, cursor = get_cursor()

    cursor.execute("""
        SELECT * FROM eleitores
        WHERE cpf = %s OR titulo_eleitor = %s
    """, (cpf, voter_id))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result is not None
