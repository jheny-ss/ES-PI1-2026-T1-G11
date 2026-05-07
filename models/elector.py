from database.connection import get_cursor
from models.voting import generate_access_key
from models.validators.cpf_validation import validate_cpf
from models.validators.voter_registration_validation import registration_validation
from models.crypto.decrypt import decrypt_hill_cipher
from models.crypto.encrypt import encrypt_hill_cipher

def list_electors():
    connection, cursor = get_cursor()

    try:
        cursor.execute("""
            SELECT id, nome, cpf, titulo_eleitor, chave_acesso, status_mesario
            FROM eleitores
        """)

        print("\nLISTA DE ELEITORES:")

        for elector in cursor.fetchall():
           
            cpf = decrypt_hill_cipher(elector['cpf'])
            chave = decrypt_hill_cipher(elector['chave_acesso'])
            print(f"{elector['id']} - {elector['nome']} - {elector['titulo_eleitor']} - {chave} - {elector['status_mesario']}")
    finally:
        cursor.close()
        connection.close()


def get_elector_by_cpf(cpf):
    connection, cursor = get_cursor()

    try:
        cpf = encrypt_hill_cipher(cpf)

        cursor.execute(
            "SELECT * FROM eleitores WHERE cpf = %s",
            (cpf,)
        )

        elector = cursor.fetchone()

        if elector:
            elector['cpf'] = decrypt_hill_cipher(elector['cpf'])
            elector['chave_acesso'] = decrypt_hill_cipher(elector['chave_acesso'])

        return elector

    finally:
        cursor.close()
        connection.close()



def create_elector(cursor, name, cpf, voter_id, access_key, is_poll_worker):
    sql = """
        INSERT INTO eleitores (nome, cpf, titulo_eleitor, chave_acesso, status_mesario)
        VALUES (%s, %s, %s, %s, %s)
    """
    cpf = encrypt_hill_cipher(cpf)
    access_key = encrypt_hill_cipher(access_key)
    cursor.execute(sql, (name, cpf, voter_id, access_key, is_poll_worker))


def delete_elector(cpf):
    connection, cursor = get_cursor()

    try:
        cpf = encrypt_hill_cipher(cpf)

        cursor.execute(
            "DELETE FROM eleitores WHERE cpf = %s",
            (cpf,)
        )

        connection.commit()

        if cursor.rowcount > 0:
            print("Eleitor removido!")
        else:
            print("Eleitor não encontrado!")

    finally:
        cursor.close()
        connection.close()

def update_elector_db(cpf, name, voter_id, is_poll_worker):
    connection, cursor = get_cursor()

    try:
        cpf = encrypt_hill_cipher(cpf)

        cursor.execute("""
            UPDATE eleitores
            SET nome = %s, titulo_eleitor = %s, status_mesario = %s
            WHERE cpf = %s
        """, (name, voter_id, is_poll_worker, cpf))

        connection.commit()

    finally:
        cursor.close()
        connection.close()



def elector_exists(cursor, cpf, voter_id):
    cpf = encrypt_hill_cipher(cpf)

    cursor.execute("""
        SELECT 1 FROM eleitores
        WHERE cpf = %s OR titulo_eleitor = %s
    """, (cpf, voter_id))

    return cursor.fetchone() is not None