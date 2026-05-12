from views.menus import print_line
from database.connection import get_cursor

from models.audit import register_error_log

def elector_choice():

    connection, cursor = get_cursor()

    try:

        cursor.execute(
            """
            SELECT
                candidatos.partido,
                COUNT(votacao.id) AS total
            FROM votacao
            INNER JOIN candidatos
                ON candidatos.id = votacao.id_candidato
            GROUP BY candidatos.partido
            """
        )

        results = cursor.fetchall()

        print_line()
        print("VOTOS POR PARTIDO".center(50))
        print_line()

        for result in results:
            print(
                f"Partido: {result['partido']} | "
                f"Total de votos: {result['total']}"
            )

    except Exception as error:

        print(error)  # MOSTRA O ERRO REAL

        register_error_log(error)

        print("Erro na apuração dos votos por partido")

    finally:

        cursor.close()
        connection.close()