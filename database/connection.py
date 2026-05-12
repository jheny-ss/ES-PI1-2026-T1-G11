import mysql.connector


def get_connection():
    """
    Cria e retorna uma conexão com o banco de dados MySQL.

    Returns:
        connection: Objeto de conexão.
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",          # ajuste conforme seu ambiente
        password="607090Jhenyfer#",          # ajuste conforme seu ambiente
        database="sistema_de_votacao"
    )


def get_cursor():
    """
    Retorna conexão e cursor configurado para dicionário.

    Returns:
        tuple: (conexao, cursor)
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    return connection, cursor
