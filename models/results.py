from views.menus import print_line
def elector_choice():


    connection, cursor = get_cursor()

    try:

        cursor.execute(
            """
            SELECT
                candidatos.partido
                COUNT (votacao.id) AS total
                FROM votacao
                INNER JOIN candidatos
                ON candidatos.id = votacao.id_cadidato
                GROUP BY cadidatos.partido
            """
        )

        results = cursor.fetchall()

        print_line()
        print("VOTOS POR PARTIDO".center(50))
        print_line()

        for politicals,total in results:
            print (f"Partido: {politicals} | Total de votos: {total}"
            )

    except Exception as error:

        register_error_log(error)

        print(
            "Erro na apuração dos votos por partido"
        )

    finally:

        cursor.close()
        connection.close()