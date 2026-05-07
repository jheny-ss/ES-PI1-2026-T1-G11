import random
from database.connection import get_cursor
from models.crypto.decrypt import decrypt_hill_cipher
from models.crypto.encrypt import encrypt_hill_cipher

def validate_poll_worker(cpf_partial, voter_id, access_key):
    """
    Valida se o usuário é um mesário (poll worker) autorizado.

    Args:
        cpf_partial (str): Primeiros 4 dígitos do CPF.
        voter_id (str): Título de eleitor.
        access_key (str): Chave de acesso do eleitor.

    Returns:
        bool: True se for um mesário válido, False caso contrário.
    """
    connection, cursor = get_cursor()

    cursor.execute("""
        SELECT status_mesario, cpf
        FROM eleitores
        WHERE titulo_eleitor = %s
          AND chave_acesso = %s
    """, (voter_id, access_key))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result is None:
        return False

    cpf_decrypted = decrypt_hill_cipher(result["cpf"])
    cpf_matches = cpf_decrypted.startswith(cpf_partial)

    return cpf_matches and bool(result["status_mesario"])


def generate_access_key(full_name):
    name_parts = full_name.strip().upper().split()

    first_name = name_parts[0]
    second_name = name_parts[1]

    letters = first_name[:2] + second_name[0]
    numbers = str(random.randint(1000, 9999))
    access_key = letters + numbers

    return access_key
    
def zeresima():
    """
    Realiza a zerésima da votação.

    Remove todos os votos registrados e redefine o status
    de votação de todos os eleitores para FALSE.

    Utilizado antes da abertura oficial da votação.
    """
    connection, cursor = get_cursor()

    try:
        # Apagar todos os votos
        cursor.execute("DELETE FROM votacao")

        # Resetar status dos eleitores
        cursor.execute("""
            UPDATE eleitores
            SET status_votacao = FALSE
        """)

        connection.commit()
        print("Votação zerada com sucesso!")

    except Exception as e:
        print("Erro ao zerar votação:", e)

    finally:
        cursor.close()
        connection.close()
