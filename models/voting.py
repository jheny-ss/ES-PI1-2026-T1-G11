import random
import string
from datetime import datetime
from database.connection import get_cursor
from models.candidate import get_candidate_by_number
from models.crypto.encrypt import (
    encrypt_hill_cipher
)
from models.crypto.decrypt import (
    decrypt_hill_cipher
)
from models.audit import (
    register_access_denied_log,
    register_double_vote_log,
    register_vote_success_log,
    register_protocol,
    register_closing_log,
    register_null_vote_log,
    register_error_log
)

# ============================================================
# VALIDAÇÃO DE MESÁRIO
# ============================================================

def validate_poll_worker(
    cpf_partial,
    voter_id,
    access_key
):
    """
    Valida se o usuário é um mesário autorizado.

    Regras:
    - título deve existir
    - chave deve ser válida
    - CPF deve corresponder
    - status_mesario deve ser TRUE

    Args:
        cpf_partial (str):
            4 primeiros dígitos do CPF.

        voter_id (str):
            Título de eleitor.

        access_key (str):
            Chave de acesso.

    Returns:
        bool:
            True se autorizado.
            False caso contrário.
    """

    connection, cursor = get_cursor()

    try:

        encrypted_key = encrypt_hill_cipher(
            access_key
        )

        encrypted_voter_id = encrypt_hill_cipher(
            voter_id
        )

        cursor.execute("""
            SELECT
                status_mesario,
                cpf
            FROM eleitores
            WHERE titulo_eleitor = %s
              AND chave_acesso = %s
        """, (encrypted_voter_id, encrypted_key))

        result = cursor.fetchone()

        # Não encontrado
        if result is None:
            return False

        decrypted_cpf = decrypt_hill_cipher(
            result["cpf"]
        )

        # CPF inválido
        if not decrypted_cpf.startswith(
            cpf_partial
        ):
            return False

        # Não é mesário
        if not result["status_mesario"]:
            return False

        return True

    except Exception as error:

        register_error_log(error)

        return False

    finally:

        cursor.close()
        connection.close()

# ============================================================
# GERAÇÃO DE CHAVE
# ============================================================

def generate_access_key(full_name):
    """
    Gera uma chave de acesso automática.

    Formato:
    - 3 letras
    - 4 números aleatórios

    Exemplo:
        ARS4821

    Args:
        full_name (str):
            Nome completo do eleitor.

    Returns:
        str:
            Chave de acesso gerada.
    """

    name_parts = (
        full_name
        .strip()
        .upper()
        .split()
    )

    first_name = name_parts[0]

    # Segurança para nomes simples
    if len(name_parts) > 1:
        second_name = name_parts[1]
    else:
        second_name = "X"

    letters = (
        first_name[:2]
        + second_name[0]
    )

    numbers = str(
        random.randint(1000, 9999)
    )

    access_key = letters + numbers

    return access_key

# ============================================================
# ZERÉSIMA
# ============================================================

def zeresima():
    """
    Realiza a zerésima da votação.

    Funcionamento:
    - remove votos anteriores
    - redefine status_votacao

    Returns:
        bool:
            True se executado.
            False caso contrário.
    """

    connection, cursor = get_cursor()

    try:

        cursor.execute(
            "DELETE FROM votacao"
        )

        cursor.execute("""
            UPDATE eleitores
            SET status_votacao = FALSE
        """)

        connection.commit()

        print(
            "Votação zerada com sucesso!"
        )

        return True

    except Exception as error:

        connection.rollback()

        register_error_log(error)

        print(
            "Erro ao realizar zerésima!"
        )

        return False

    finally:

        cursor.close()
        connection.close()

# ============================================================
# PROTOCOLO
# ============================================================

def generate_voting_protocol(
    candidate_number
):
    """
    Gera protocolo oficial da votação.

    Padrão:
    V + 2 letras + 26 +
    número candidato +
    5 dígitos aleatórios

    Exemplo:
        VAB261512345

    Args:
        candidate_number (str | None)

    Returns:
        str
    """

    UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    DIGITS = '0123456789'

    letters = ''.join(
        random.choices(UPPERCASE, k=2)
    )

    year = "26"

    if candidate_number is None:
        number = "00"

    else:
        number = str(
            candidate_number
        ).zfill(2)

    digits = ''.join(
        random.choices(DIGITS, k=5)
    )
    
    return (
        f"V{letters}"
        f"{year}"
        f"{number}"
        f"{digits}"
    )

# ============================================================
# IDENTIFICAÇÃO DO ELEITOR
# ============================================================

def identify_voter(
    voter_id,
    cpf_partial,
    access_key
):
    """
    Identifica eleitor pelas credenciais.

    Args:
        voter_id (str)
        cpf_partial (str)
        access_key (str)

    Returns:
        dict | None
    """

    connection, cursor = get_cursor()

    try:

        encrypted_voter_id = encrypt_hill_cipher(
            voter_id
        )

        encrypted_key = encrypt_hill_cipher(
            access_key
        )

        cursor.execute("""
            SELECT
                id,
                nome,
                cpf,
                status_votacao
            FROM eleitores
            WHERE titulo_eleitor = %s
              AND chave_acesso = %s
        """, (
            encrypted_voter_id,
            encrypted_key
        ))

        result = cursor.fetchone()

        if result is None:
            return None

        decrypted_cpf = decrypt_hill_cipher(
            result["cpf"]
        )

        if not decrypted_cpf.startswith(
            cpf_partial
        ):
            return None

        return result

    except Exception as error:

        register_error_log(error)

        return None

    finally:

        cursor.close()
        connection.close()

# ============================================================
# REGISTRO DO VOTO
# ============================================================

def register_vote(
    voter_id,
    candidate_id,
    protocol
):
    """
    Registra o voto no banco.

    Funcionamento:
    - salva voto
    - salva protocolo criptografado
    - atualiza status_votacao

    Args:
        voter_id (str)
        candidate_id (int | None)
        protocol (str)

    Returns:
        bool
    """

    connection, cursor = get_cursor()

    try:

        encrypted_protocol = (
            encrypt_hill_cipher(protocol)
        )

        encrypted_voter_id = (
            encrypt_hill_cipher(voter_id)
        )

        vote_date = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute("""
            INSERT INTO votacao (
                protocolo_criptografado,
                id_candidato,
                data_voto
            )
            VALUES (%s, %s, %s)
        """, (
            encrypted_protocol,
            candidate_id,
            vote_date
        ))

        cursor.execute("""
            UPDATE eleitores
            SET status_votacao = TRUE
            WHERE titulo_eleitor = %s
        """, (encrypted_voter_id,))

        connection.commit()

        return True

    except Exception as error:

        connection.rollback()

        register_error_log(error)

        print(
            "Erro ao registrar voto!"
        )

        return False

    finally:

        cursor.close()
        connection.close()

# ============================================================
# FLUXO DE VOTAÇÃO
# ============================================================

def cast_vote():
    """
    Executa o fluxo completo da votação.

    Fluxo:
    1. Identifica eleitor
    2. Verifica voto duplo
    3. Captura candidato
    4. Confirma voto
    5. Gera protocolo
    6. Registra voto
    7. Registra auditoria
    """

    # ========================================================
    # IDENTIFICAÇÃO
    # ========================================================

    voter_id = input(
        "Título de eleitor: "
    )

    cpf_partial = input(
        "4 primeiros dígitos do CPF: "
    )

    access_key = input(
        "Chave de acesso: "
    )

    voter = identify_voter(
        voter_id,
        cpf_partial,
        access_key
    )

    # Acesso negado
    if voter is None:

        print(
            "Dados inválidos! "
            "Acesso negado."
        )

        register_access_denied_log()

        return

    # Voto duplo
    if voter["status_votacao"]:

        print(
            "Este eleitor já votou!"
        )

        register_double_vote_log()

        return

    # ========================================================
    # ESCOLHA DO CANDIDATO
    # ========================================================

    candidate_id = None
    candidate_number = None

    confirmed = False

    while not confirmed:

        number = input(
            "Digite o número "
            "do candidato: "
        )

        candidate = (
            get_candidate_by_number(number)
        )

        # Candidato válido
        if candidate:

            print(
                f"\nCandidato: "
                f"{candidate['nome']}"
            )

            print(
                f"Número: "
                f"{candidate['numero_de_votacao']}"
            )

            print(
                f"Partido: "
                f"{candidate['partido']}"
            )

            candidate_id = candidate["id"]

            candidate_number = (
                candidate[
                    "numero_de_votacao"
                ]
            )

        # Voto nulo
        else:

            print(
                "Candidato não encontrado."
            )

            print(
                "O voto será "
                "registrado como NULO."
            )

            register_null_vote_log()

            candidate_id = None
            candidate_number = None

        confirm = input(
            "\nConfirma o voto? "
            "(Sim/Não): "
        ).strip().lower()

        if confirm == "sim":

            confirmed = True

        else:

            print(
                "\nVoto cancelado."
            )

    # ========================================================
    # GERAÇÃO DE PROTOCOLO
    # ========================================================

    protocol = generate_voting_protocol(
        candidate_number
    )

    # ========================================================
    # REGISTRO DO VOTO
    # ========================================================

    success = register_vote(
        voter_id,
        candidate_id,
        protocol
    )

    if success:

        print(
            "\nVoto confirmado!"
        )

        print(
            f"Guarde seu protocolo: "
            f"{protocol}"
        )

        # Auditoria
        register_vote_success_log(
            protocol
        )

        register_protocol(
            protocol
        )

    else:

        print(
            "Erro ao registrar voto."
        )

# ============================================================
# ENCERRAMENTO DA VOTAÇÃO
# ============================================================

def finalize_voting(
    cpf_partial,
    voter_id,
    access_key
):
    """
    Finaliza oficialmente a votação.

    Regras:
    - apenas mesário autorizado
    - confirmação obrigatória
    - revalidação da chave

    Args:
        cpf_partial (str)
        voter_id (str)
        access_key (str)

    Returns:
        bool
    """

    # Validação inicial
    if not validate_poll_worker(
        cpf_partial,
        voter_id,
        access_key
    ):

        print(
            "Acesso negado!"
        )

        register_access_denied_log()

        return False

    # Confirmação
    confirm = input(
        "Deseja realmente "
        "encerrar a votação? "
        "(Sim/Não): "
    ).strip().lower()

    if confirm != "sim":

        print(
            "Encerramento cancelado."
        )

        return False

    # Revalidação da chave
    access_key_confirm = input(
        "Digite sua chave "
        "novamente: "
    ).strip()

    if not validate_poll_worker(
        cpf_partial,
        voter_id,
        access_key_confirm
    ):

        print(
            "Chave inválida!"
        )

        register_access_denied_log()

        return False

    print(
        "Votação encerrada "
        "com sucesso!"
    )

    register_closing_log()

    return True
