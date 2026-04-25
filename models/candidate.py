from database.connection import get_cursor


def listar_candidatos():
    """
    Lista todos os candidatos.
    """
    conexao, cursor = get_cursor()

    cursor.execute("SELECT * FROM candidatos")

    print("\n LISTA DE CANDIDATOS:")
    for c in cursor.fetchall():
        print(f"{c['nome']} - {c['numero_de_votacao']} - {c['partido']}")

    cursor.close()
    conexao.close()


def buscar_candidato(numero):
    """
    Busca candidato pelo número.
    """
    conexao, cursor = get_cursor()

    cursor.execute(
        "SELECT * FROM candidatos WHERE numero_de_votacao = %s",
        (numero,)
    )

    candidato = cursor.fetchone()

    cursor.close()
    conexao.close()

    return candidato


def inserir_candidato(nome, numero, partido):
    """
    Cadastra um novo candidato.
    """

    conexao, cursor = get_cursor()
    if numero.isdigit():
            cursor.execute("SELECT id FROM candidatos WHERE numero_de_votacao = %s", (numero,))
            resultado = cursor.fetchone()
    
            if resultado is not None:
                print("Número de candidato já existe!")
                cursor.close()
                conexao.close()
                return

    sql = """
        INSERT INTO candidatos (nome, numero_de_votacao, partido)
        VALUES (%s, %s, %s)
    """

    cursor.execute(sql, (nome, numero, partido))
    conexao.commit()

    print("Candidato cadastrado!")

    cursor.close()
    conexao.close()


def remover_candidato(numero):
    """
    Remove candidato pelo número.
    """
    conexao, cursor = get_cursor()

    cursor.execute(
        "DELETE FROM candidatos WHERE numero_de_votacao = %s",
        (numero,)
    )
    conexao.commit()

    print("Candidato removido!")

    cursor.close()
    conexao.close()

def editar_candidato():
    """
    Edita candidato pelo número.
    """
    numero = input("Número do candidato: ")

    conexao, cursor = get_cursor()
    cursor.execute("SELECT id FROM candidatos WHERE numero_de_votacao = %s", (numero,))
    resultado = cursor.fetchone()

    if resultado is None:
        print("Candidato não encontrado!")
        cursor.close()
        conexao.close()
        return

    # Só pede os dados se o candidato existir
    nome    = input("Novo nome: ")
    partido = input("Novo partido: ")

    cursor.execute(
        "UPDATE candidatos SET nome = %s, partido = %s WHERE numero_de_votacao = %s",
        (nome, partido, numero)
    )
    conexao.commit()

    print("Candidato atualizado com sucesso!")
    cursor.close()
    conexao.close()
