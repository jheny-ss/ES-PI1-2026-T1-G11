# ============================================================
# CIFRA DE HILL - CRIPTOGRAFIA
# ============================================================

"""
Módulo responsável pela criptografia de textos
utilizando a Cifra de Hill 2x2.

A criptografia funciona através de:
- Matrizes
- Álgebra linear
- Aritmética modular (mod 36)

O sistema suporta:
- Letras
- Números

A chave utilizada é:

| 2 1 |
| 3 2 |
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
# PREPARAÇÃO DO TEXTO
# ============================================================

def normalize_text(text):
    """
    Normaliza o texto antes da criptografia.

    Regras:
    - Remove espaços
    - Remove caracteres especiais
    - Mantém letras e números
    - Converte para maiúsculo
    - Se tamanho for ímpar adiciona X

    Args:
        text (str):
            Texto original.

    Returns:
        str:
            Texto normalizado.
    """

    text = text.upper()

    filtered_text = ""

    for character in text:

        if character in ALPHABET:
            filtered_text += character

    # Padding
    if len(filtered_text) % 2 != 0:
        filtered_text += "X"

    return filtered_text


# ============================================================
# CRIPTOGRAFIA
# ============================================================

def encrypt_hill_cipher(text):
    """
    Criptografa um texto utilizando
    a Cifra de Hill.

    Args:
        text (str):
            Texto original.

    Returns:
        str:
            Texto criptografado.
    """

    text = normalize_text(text)

    encrypted_text = ""

    for index in range(0, len(text), 2):

        first_character = text[index]
        second_character = text[index + 1]

        x1 = ALPHABET.index(first_character)
        x2 = ALPHABET.index(second_character)

        # Multiplicação matricial
        y1 = (
            KEY_MATRIX[0][0] * x1 +
            KEY_MATRIX[0][1] * x2
        )

        y2 = (
            KEY_MATRIX[1][0] * x1 +
            KEY_MATRIX[1][1] * x2
        )

        # Aplicação do módulo
        y1 = euclidean_mod(y1, MOD)
        y2 = euclidean_mod(y2, MOD)

        # Conversão para caracteres
        encrypted_text += ALPHABET[y1]
        encrypted_text += ALPHABET[y2]

    return encrypted_text
