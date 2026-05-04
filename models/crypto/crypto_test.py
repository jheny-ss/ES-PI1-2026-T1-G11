from models.crypto.encrypt import encrypt_hill_cipher
from models.crypto.decrypt import decrypt_hill_cipher


# ============================================================
# TESTES - CIFRA DE HILL
# ============================================================

"""
Arquivo responsável por validar o funcionamento
da criptografia e descriptografia do sistema.

Objetivos:
- Validar criptografia
- Validar descriptografia
- Garantir integridade dos dados
- Garantir retorno correto do texto original

EXECUÇÃO:

python -m models.crypto.crypto_test
"""


# ============================================================
# ALFABETO SUPORTADO
# ============================================================

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


# ============================================================
# FUNÇÃO AUXILIAR
# ============================================================

def execute_test(original_text):
    """
    Executa teste completo de criptografia.

    Fluxo:
    - Criptografa
    - Descriptografa
    - Compara resultado

    Args:
        original_text (str):
            Texto original do teste.
    """

    print("=" * 60)
    print(f"TEXTO ORIGINAL: {original_text}")

    # ========================================================
    # CRIPTOGRAFIA
    # ========================================================

    encrypted_text = encrypt_hill_cipher(original_text)

    print(f"TEXTO CRIPTOGRAFADO: {encrypted_text}")

    # ========================================================
    # DESCRIPTOGRAFIA
    # ========================================================

    decrypted_text = decrypt_hill_cipher(encrypted_text)

    print(f"TEXTO DESCRIPTOGRAFADO: {decrypted_text}")

    # ========================================================
    # NORMALIZAÇÃO PARA COMPARAÇÃO
    # ========================================================

    normalized_original = ""

    for character in original_text.upper():

        if character in ALPHABET:
            normalized_original += character

    # ========================================================
    # VALIDAÇÃO
    # ========================================================

    if normalized_original == decrypted_text:
        print("RESULTADO: TESTE APROVADO")
    else:
        print("RESULTADO: TESTE REPROVADO")

    print("=" * 60)
    print()


# ============================================================
# TESTE 1
# PALAVRA PAR
# ============================================================

print("\nTESTE 1 - PALAVRA COM QUANTIDADE PAR\n")

execute_test("VOTO")


# ============================================================
# TESTE 2
# PALAVRA ÍMPAR
# ============================================================

print("\nTESTE 2 - PALAVRA ÍMPAR\n")

execute_test("CPF")


# ============================================================
# TESTE 3
# TEXTO COM ESPAÇOS
# ============================================================

print("\nTESTE 3 - TEXTO COM ESPAÇOS\n")

execute_test("TITULO ELEITOR")


# ============================================================
# TESTE 4
# TEXTO COM NÚMEROS
# ============================================================

print("\nTESTE 4 - TEXTO COM NÚMEROS\n")

execute_test("CPF123")


# ============================================================
# TESTE 5
# TEXTO COM CARACTERES ESPECIAIS
# ============================================================

print("\nTESTE 5 - TEXTO COM CARACTERES ESPECIAIS\n")

execute_test("VOTO!!!")


# ============================================================
# TESTE 6
# CPF
# ============================================================

print("\nTESTE 6 - CPF\n")

execute_test("52998224725")


# ============================================================
# TESTE 7
# CHAVE DE ACESSO
# ============================================================

print("\nTESTE 7 - CHAVE DE ACESSO\n")

execute_test("ABC123")


# ============================================================
# TESTE 8
# PROTOCOLO DE VOTAÇÃO
# ============================================================

print("\nTESTE 8 - PROTOCOLO DE VOTAÇÃO\n")

execute_test("VRT269950134")


# ============================================================
# TESTE 9
# NOME DE ELEITOR
# ============================================================

print("\nTESTE 9 - NOME DE ELEITOR\n")

execute_test("ARTHUR")


# ============================================================
# TESTE 10
# TEXTO LONGO
# ============================================================

print("\nTESTE 10 - TEXTO LONGO\n")

execute_test(
    "SISTEMADEAUDITORIADEVOTACAO"
)


print("\nTODOS OS TESTES FINALIZADOS\n")
