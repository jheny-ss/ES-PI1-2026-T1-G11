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

def statistic_voters():

    connection, cursor = get_cursor()

    try:

        cursor.execute(
            """
            SELECT id,
            COUNT(*) as total
            FROM eleitores
            """ 
            )
        
        
        total_result = cursor.fetchone()
        total = total_result['total']
        
        
        cursor.execute(
            """SELECT votacao.id_candidatos,
            COUNT (id) as total_comparecidos
            FROM eleitores
            INNER JOIN votacao
            ON votacao.id = eleitores.id
            """
            )
        
        comparecidos_result = cursor.fetchone()
        total_comparecidos = comparecidos_result['total_comparecidos']
        results = cursor.fetchall()

        print_line()
        print("ESTATÍSTICA".center(50))
        print_line()

        for result in results:
            print(
                f"Eleitores comparecidos na votação: {result['total_comparecidos']} | "
                f"Total de eleitores: {result['total']} | "
                f"Porcentagem de participação: {((total_comparecidos*100)/total): .2f}%" 
            )

    except Exception as error:

        print(error)  # MOSTRA O ERRO REAL

        register_error_log(error)

        print("Erro no cálculo de eleitores")

    finally:

        cursor.close()
        connection.close()