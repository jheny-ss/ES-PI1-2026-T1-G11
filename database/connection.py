import mysql.connector


def get_connection():
    """
    Cria e retorna uma conexão com o banco de dados MySQL.

    Args:
        None

    Returns:
        mysql.connector.connection.MySQLConnection:
            Objeto de conexão com o banco de dados
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",          # ajuste conforme seu ambiente
        password="Juju@0707",          # ajuste conforme seu ambiente
        database="sistema_de_votacao"
    )


def get_cursor():
    """
    Cria e retorna uma conexão e um cursor configurado
    para retornar resultados em formato de dicionário.

    Args:
        None

    Returns:
        tuple:
            Tupla contendo a conexão com o banco de dados
            e o cursor configurado para dicionário.
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    return connection, cursor
