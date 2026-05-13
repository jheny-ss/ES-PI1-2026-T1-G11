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
            ORDER BY total DESC
            """
        )

        results = cursor.fetchall()

        print_line()
        print("VOTOS POR PARTIDO".center(50))
        print_line()

        if results:

            for result in results:

                print(
                    f"Partido: {result['partido']} | "
                    f"Total de votos: {result['total']}"
                )

        else:

            print("Nenhum voto registrado.")

        print_line()

    except Exception as error:

        print(error)

        register_error_log(error)

        print("Erro na apuração dos votos por partido")

    finally:

        cursor.close()
        connection.close()


def statistic_voters():

    connection, cursor = get_cursor()

    try:

        # TOTAL DE ELEITORES
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM eleitores
            """
        )

        total_result = cursor.fetchone()

        total = total_result['total']

        # TOTAL DE COMPARECIMENTOS
        cursor.execute(
            """
            SELECT COUNT(*) AS total_comparecidos
            FROM votacao
            """
        )

        comparecidos_result = cursor.fetchone()

        total_comparecidos = (
            comparecidos_result['total_comparecidos']
        )

        # PORCENTAGEM
        porcentagem = 0

        if total > 0:

            porcentagem = (
                total_comparecidos * 100
            ) / total

        print_line()
        print("ESTATÍSTICA".center(50))
        print_line()

        print(
            f"Eleitores comparecidos: "
            f"{total_comparecidos}"
        )

        print(
            f"Total de eleitores: "
            f"{total}"
        )

        print(
            f"Porcentagem de participação: "
            f"{porcentagem:.2f}%"
        )

        print_line()

    except Exception as error:

        print(error)

        register_error_log(error)

        print("Erro no cálculo de eleitores")

    finally:

        cursor.close()
        connection.close()


def ballot_box():
    """
    Exibe o boletim de urna com os votos consolidados
    por candidato em ordem alfabética e declara
    o vencedor da eleição.

    Returns:
        None
    """

    connection, cursor = get_cursor()

    try:

        cursor.execute(
            """
            SELECT
                candidatos.nome,
                candidatos.numero_de_votacao,
                candidatos.partido,
                COUNT(votacao.id) AS total_votos
            FROM candidatos
            LEFT JOIN votacao
                ON votacao.id_candidato = candidatos.id
            GROUP BY
                candidatos.id,
                candidatos.nome,
                candidatos.numero_de_votacao,
                candidatos.partido
            ORDER BY candidatos.nome ASC
            """
        )

        results = cursor.fetchall()

        # VOTOS NULOS
        cursor.execute(
            """
            SELECT COUNT(*) AS total_nulos
            FROM votacao
            WHERE id_candidato IS NULL
            """
        )

        nulos = cursor.fetchone()['total_nulos']

        print_line()
        print("BOLETIM DE URNA".center(50))
        print_line()

        # LISTAGEM DOS CANDIDATOS
        for result in results:

            print(
                f"Candidato: {result['nome']} | "
                f"Número: {result['numero_de_votacao']} | "
                f"Partido: {result['partido']} | "
                f"Votos: {result['total_votos']}"
            )

        print(f"\nVotos nulos: {nulos}")

        print_line()

        # VERIFICA SE EXISTEM CANDIDATOS
        if results:

            # MAIOR QUANTIDADE DE VOTOS
            maior_total = max(
                candidato['total_votos']
                for candidato in results
            )

            # CANDIDATOS EMPATADOS
            vencedores = [

                candidato

                for candidato in results

                if candidato['total_votos']
                == maior_total
            ]

            # EMPATE
            if len(vencedores) > 1:

                print(
                    "EMPATE NA ELEIÇÃO".center(50)
                )

                print_line()

                for candidato in vencedores:

                    print(
                        f"Nome:    {candidato['nome']}\n"
                        f"Número:  "
                        f"{candidato['numero_de_votacao']}\n"
                        f"Partido: "
                        f"{candidato['partido']}\n"
                        f"Votos:   "
                        f"{candidato['total_votos']}"
                    )

                    print_line()

            # VENCEDOR ÚNICO
            else:

                vencedor = vencedores[0]

                print(
                    "VENCEDOR DA ELEIÇÃO".center(50)
                )

                print_line()

                print(
                    f"Nome:    {vencedor['nome']}\n"
                    f"Número:  "
                    f"{vencedor['numero_de_votacao']}\n"
                    f"Partido: "
                    f"{vencedor['partido']}\n"
                    f"Votos:   "
                    f"{vencedor['total_votos']}"
                )

        else:

            print(
                "Nenhum candidato registrado."
                .center(50)
            )

        print_line()

    except Exception as error:

        print(error)

        register_error_log(error)

        print("Erro ao gerar o boletim de urna.")

    finally:

        cursor.close()
        connection.close()


def integrity_validation():
    """
    Valida a integridade da eleição comparando
    o total de votos registrados na urna
    com o total de eleitores com status
    'Já Votou'.

    Returns:
        None
    """

    connection, cursor = get_cursor()

    try:

        # TOTAL DE VOTOS
        cursor.execute(
            """
            SELECT COUNT(*) AS total_votos
            FROM votacao
            """
        )

        total_votos = (
            cursor.fetchone()['total_votos']
        )

        # TOTAL DE ELEITORES QUE JÁ VOTARAM
        cursor.execute(
            """
            SELECT COUNT(*) AS total_ja_votou
            FROM eleitores
            WHERE status_votacao = TRUE
            """
        )

        total_ja_votou = (
            cursor.fetchone()['total_ja_votou']
        )

        print_line()

        print(
            "VALIDAÇÃO DE INTEGRIDADE"
            .center(50)
        )

        print_line()

        print(
            f"Votos registrados na urna: "
            f"{total_votos}"
        )

        print(
            f"Eleitores com status "
            f"'Já Votou': "
            f"{total_ja_votou}"
        )

        print_line()

        # VALIDAÇÃO
        if total_votos == total_ja_votou:

            print(
                "ÍNTEGRA: "
                "Os números coincidem. "
                "Eleição válida."
                .center(50)
            )

        else:

            diferenca = abs(
                total_votos - total_ja_votou
            )

            print(
                "INCONSISTÊNCIA DETECTADA!"
                .center(50)
            )

            print(
                f"Diferença: "
                f"{diferenca} registro(s) "
                f"divergente(s)."
            )

        print_line()

    except Exception as error:

        print(error)

        register_error_log(error)

        print("Erro na validação de integridade.")

    finally:

        cursor.close()
        connection.close()