# ============================================================
# CIFRA DE HILL - DESCRIPTOGRAFIA
# ============================================================

"""
Módulo responsável pela descriptografia
utilizando a Cifra de Hill 2x2.

O algoritmo utiliza:
- Matriz inversa
- Álgebra linear
- Aritmética modular

Sistema compatível com:
- Letras
- Números
"""


# ============================================================
# ALFABETO
# ============================================================

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


# ============================================================
# MÓDULO
# ============================================================

MOD = len(ALPHABET)


# ============================================================
# MATRIZ CHAVE
# ============================================================

KEY_MATRIX = [
    [2, 1],
    [3, 2]
]


# ============================================================
# TABELA DE INVERSOS MODULARES
# ============================================================

MODULAR_INVERSES = {
    1: 1,
    5: 29,
    7: 31,
    11: 23,
    13: 25,
    17: 17,
    19: 19,
    23: 11,
    25: 13,
    29: 5,
    31: 7,
    35: 35
}


# ============================================================
# FUNÇÃO DE MÓDULO EUCLIDIANO
# ============================================================

def euclidean_mod(number, mod):
    """
    Realiza módulo euclidiano.

    Args:
        number (int):
            Número a ser modulado.

        mod (int):
            Valor do módulo.

    Returns:
        int:
            Resultado positivo.
    """

    return ((number % mod) + mod) % mod


# ============================================================
# MATRIZ INVERSA
# ============================================================

def generate_inverse_matrix():
    """
    Gera a matriz inversa da chave.

    Returns:
        list:
            Matriz inversa 2x2.
    """

    determinant = (
        KEY_MATRIX[0][0] * KEY_MATRIX[1][1]
        -
        KEY_MATRIX[0][1] * KEY_MATRIX[1][0]
    )

    determinant = euclidean_mod(determinant, MOD)

    inverse = MODULAR_INVERSES[determinant]

    inverse_matrix = [

        [
            inverse * KEY_MATRIX[1][1],
            inverse * (-KEY_MATRIX[0][1])
        ],

        [
            inverse * (-KEY_MATRIX[1][0]),
            inverse * KEY_MATRIX[0][0]
        ]
    ]

    for row in range(2):

        for column in range(2):

            inverse_matrix[row][column] = euclidean_mod(
                inverse_matrix[row][column],
                MOD
            )

    return inverse_matrix


# ============================================================
# DESCRIPTOGRAFIA
# ============================================================

def decrypt_hill_cipher(cipher_text):
    """
    Descriptografa um texto utilizando
    a Cifra de Hill.

    Args:
        cipher_text (str):
            Texto criptografado.

    Returns:
        str:
            Texto descriptografado.
    """

    cipher_text = cipher_text.upper()

    inverse_matrix = generate_inverse_matrix()

    decrypted_text = ""

    for index in range(0, len(cipher_text), 2):

        first_character = cipher_text[index]
        second_character = cipher_text[index + 1]

        y1 = ALPHABET.index(first_character)
        y2 = ALPHABET.index(second_character)

        # Multiplicação matricial
        x1 = (
            inverse_matrix[0][0] * y1 +
            inverse_matrix[0][1] * y2
        )

        x2 = (
            inverse_matrix[1][0] * y1 +
            inverse_matrix[1][1] * y2
        )

        # Aplicação do módulo
        x1 = euclidean_mod(x1, MOD)
        x2 = euclidean_mod(x2, MOD)

        # Conversão para caracteres
        decrypted_text += ALPHABET[x1]
        decrypted_text += ALPHABET[x2]

    # Remove padding final
    if decrypted_text.endswith("X"):
        decrypted_text = decrypted_text[:-1]

    return decrypted_text
