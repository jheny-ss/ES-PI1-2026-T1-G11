from database.connection import get_cursor


def listar_eleitores():
    """
    Lista todos os eleitores.
    """
    conexao, cursor = get_cursor()

    cursor.execute("SELECT id, nome, titulo_eleitor FROM eleitores")

    print("\nLISTA DE ELEITORES:")
    for e in cursor.fetchall():
        print(f"{e['id']} - {e['nome']} - {e['titulo_eleitor']}")

    cursor.close()
    conexao.close()


def buscar_eleitor(cpf):
    """
    Busca eleitor pelo CPF.
    """
    conexao, cursor = get_cursor()

    cursor.execute("SELECT * FROM eleitores WHERE cpf = %s", (cpf,))
    eleitor = cursor.fetchone()

    cursor.close()
    conexao.close()

    return eleitor


def inserir_eleitor(nome, cpf, titulo, chave):
    """
    Cadastra um novo eleitor.
    """
    conexao, cursor = get_cursor()

    sql = """
        INSERT INTO eleitores (nome, cpf, titulo_eleitor, chave_acesso)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (nome, cpf, titulo, chave))
    conexao.commit()

    print("Eleitor cadastrado!")

    cursor.close()
    conexao.close()


def remover_eleitor(cpf):
    """
    Remove eleitor pelo CPF.
    """
    conexao, cursor = get_cursor()

    cursor.execute("DELETE FROM eleitores WHERE cpf = %s", (cpf,))
    conexao.commit()

    print("Eleitor removido!")

    cursor.close()
    conexao.close()


def editar_eleitor():
    """
    Edita eleitor pelo CPF.
    """
    cpf = input("CPF do eleitor: ")

    conexao, cursor = get_cursor()
    cursor.execute("SELECT id FROM eleitores WHERE cpf = %s", (cpf,))
    resultado = cursor.fetchone()

    if resultado is None:
        print("Eleitor não encontrado!")
        cursor.close()
        conexao.close()
        return

    # Só pede os dados se o eleitor existir
    nome   = input("Novo nome: ")
    titulo = input("Novo título: ")
    chave  = input("Nova chave: ")

    cursor.execute(
    "UPDATE eleitores SET nome = %s, titulo_eleitor = %s, chave_acesso = %s WHERE cpf = %s",
    (nome, titulo, chave, cpf)
    )
    conexao.commit()

    print("Eleitor atualizado com sucesso!")
    cursor.close()
    conexao.close()
