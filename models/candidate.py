from database.connection import get_cursor


def list_candidates():
    """
    Lista todos os candidatos.
    """
    connection, cursor = get_cursor()

    cursor.execute("SELECT * FROM candidatos")

    print("\n LISTA DE CANDIDATOS:")
    for candidate  in cursor.fetchall():
        print(f"{candidate['nome']} - {candidate['numero_de_votacao']} - {candidate['partido']}")

    cursor.close()
    connection.close()


def get_candidate_by_number(number):
    """
    Busca candidato pelo número.
    """
    connection, cursor = get_cursor()

    cursor.execute(
        "SELECT * FROM candidatos WHERE numero_de_votacao = %s",
        (number,)
    )

    candidate = cursor.fetchone()

    cursor.close()
    connection.close()

    return candidate


def create_candidate(name, number, party):
    """
    Cadastra um novo candidato.
    """

    connection, cursor = get_cursor()
    if number.isdigit():
            cursor.execute("SELECT id FROM candidatos WHERE numero_de_votacao = %s", (number,))
            result  = cursor.fetchone()

            if result  is not None:
                print("Número de candidato já existe!")
                cursor.close()
                connection.close()
                return

    sql = """
        INSERT INTO candidatos (nome, numero_de_votacao, partido)
        VALUES (%s, %s, %s)
    """

    cursor.execute(sql, (name, number, party))
    connection.commit()

    print("Candidato cadastrado!")

    cursor.close()
    connection.close()


def delete_candidate(number):
    connection, cursor = get_cursor()

    cursor.execute(
        "DELETE FROM candidatos WHERE numero_de_votacao = %s",
        (number,)
    )
    connection.commit()

    if cursor.rowcount > 0:
        print("Candidato removido!")
    else:
        print("Candidato não encontrado!")

    cursor.close()
    connection.close()

def update_candidate():
    """
    Edita candidato pelo número.
    """
    connection, cursor = get_cursor()

    found = False
    number = None

    while not found:
        number = input("Número do candidato: ")

        cursor.execute(
            "SELECT id FROM candidatos WHERE numero_de_votacao = %s",
            (number,)
        )
        result = cursor.fetchone()

        if result:
            found = True
        else:
            print("Candidato não encontrado! Tente novamente.\n")

    # Só chega aqui se EXISTE candidato
    name = input("Novo nome: ")
    party = input("Novo partido: ")

    cursor.execute(
        "UPDATE candidatos SET nome = %s, partido = %s WHERE numero_de_votacao = %s",
        (name, party, number)
    )
    connection.commit()

    print("Candidato atualizado com sucesso!")

    cursor.close()
    connection.close()