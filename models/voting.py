import random
import string
from database.connection import get_cursor


def validar_mesario(cpf_parcial, titulo, chave):
    conexao, cursor = get_cursor()

    cursor.execute("""
        SELECT status_mesario 
        FROM eleitores 
        WHERE LEFT(cpf, 4) = %s 
        AND titulo_eleitor = %s 
        AND chave_acesso = %s
    """, (cpf_parcial, titulo, chave))

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado is not None and bool(resultado["status_mesario"])



def gerar_chave_acesso():
   chave = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
   return chave

def zeresima():
    conexao, cursor = get_cursor()

    try:
        # Apagar todos os votos
        cursor.execute("DELETE FROM votacao")

        # Resetar status dos eleitores
        cursor.execute("""
            UPDATE eleitores
            SET status_votacao = FALSE
        """)

        conexao.commit()
        print("Votação zerada com sucesso!")

    except Exception as e:
        print("Erro ao zerar votação:", e)

    finally:
        cursor.close()
        conexao.close()