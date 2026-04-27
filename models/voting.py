import random
import string
from database.connection import get_cursor


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
        SELECT status_mesario
        FROM eleitores
        WHERE LEFT(cpf, 4) = %s
        AND titulo_eleitor = %s
        AND chave_acesso = %s
    """, (cpf_partial, voter_id, access_key))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result is not None and bool(result["status_mesario"])



def generate_access_key():
   """
    Gera uma chave de acesso aleatória.

    A chave é composta por letras maiúsculas e números,
    com tamanho fixo de 6 caracteres.

    Returns:
        str: Chave de acesso gerada.
    """
   access_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
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
