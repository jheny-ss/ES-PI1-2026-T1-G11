import random
import string
from database.connection import get_cursor
import random
import string
from models.crypto.encrypt import encrypt_hill_cipher
from models.crypto.decrypt import decrypt_hill_cipher
from datetime import datetime
from models.audit import (
    register_access_denied_log,
    register_double_vote_log,
    register_vote_success_log,
    register_protocol
)


def validate_poll_worker(cpf_partial, voter_id, access_key):
    """
    Valida se o usuário é um mesário (poll worker) autorizado.

    Args:
        cpf_partial (str): Primeiros 4 dígitos do CPF.
        voter_id (str): Título de eleitor.
        access_key (str): Chave de acesso do eleitor.

    Returns:
        bool: True se for um mesário válido, False caso contrário.
    """
    connection, cursor = get_cursor()

    cursor.execute("""
        SELECT status_mesario
        FROM eleitores
        WHERE LEFT(cpf, 4) = %s
        AND titulo_eleitor = %s
        AND chave_acesso = %s
    """, (cpf_partial, voter_id, access_key))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result is not None and bool(result["status_mesario"])



def generate_access_key():
   """
    Gera uma chave de acesso aleatória.

    A chave é composta por letras maiúsculas e números,
    com tamanho fixo de 6 caracteres.

    Returns:
        str: Chave de acesso gerada.
    """
   access_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
   return access_key

def zeresima():
    """
    Realiza a zerésima da votação.

    Remove todos os votos registrados e redefine o status
    de votação de todos os eleitores para FALSE.

    Utilizado antes da abertura oficial da votação.
    """
    connection, cursor = get_cursor()

    try:
        # Apagar todos os votos
        cursor.execute("DELETE FROM votacao")

        # Resetar status dos eleitores
        cursor.execute("""
            UPDATE eleitores
            SET status_votacao = FALSE
        """)

        connection.commit()
        print("Votação zerada com sucesso!")

    except Exception as e:
        print("Erro ao zerar votação:", e)

    finally:
        cursor.close()
        connection.close()



def generate_voting_protocol(candidate_number):
    """
    Gera o protocolo de votação do eleitor.

    Args:
        candidate_number (int or None): Número do candidato votado.

    Returns:
        str: Protocolo original no formato VXX26NNYYYYY.
    """
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    year = "26"
    number = str(candidate_number).zfill(2) if candidate_number else "00"
    digits = ''.join(random.choices(string.digits, k=5))
    return f"V{letters}{year}{number}{digits}"



def identify_voter(voter_id, cpf_partial, access_key):
    """
    Busca o eleitor no banco validando as credenciais.

    Args:
        voter_id (str): Título de eleitor.
        cpf_partial (str): 4 primeiros dígitos do CPF.
        access_key (str): Chave de acesso digitada pelo eleitor.

    Returns:
        dict or None: Dados do eleitor se encontrado, None caso contrário.
    """
    connection, cursor = get_cursor()

    encrypted_key = encrypt_hill_cipher(access_key)

    cursor.execute("""
        SELECT id, nome, cpf, status_votacao
        FROM eleitores
        WHERE titulo_eleitor = %s
        AND chave_acesso = %s
    """, (voter_id, encrypted_key))

    result = cursor.fetchone()
    cursor.close()
    connection.close()

    if result is None:
        return None

    # Descriptografa o CPF e compara os 4 primeiros dígitos
    decrypted_cpf = decrypt_hill_cipher(result["cpf"])

    if not decrypted_cpf.startswith(cpf_partial):
        return None

    return result



def get_candidate_by_number(number):
    """
    Busca um candidato pelo número.

    Args:
        number (str): Número do candidato digitado.

    Returns:
        dict or None: Dados do candidato ou None se não existir.
    """
    connection, cursor = get_cursor()

    cursor.execute("""
        SELECT id, nome, numero_de_votacao, partido
        FROM candidatos
        WHERE numero_de_votacao = %s
    """, (number,))

    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result



def register_vote(voter_id, candidate_id, protocol):
    """
    Registra o voto na tabela votacao e atualiza o status do eleitor.

    Args:
        voter_id (str): Título do eleitor para atualizar status.
        candidate_id (int or None): ID do candidato. None = voto nulo.
        protocol (str): Protocolo original gerado para o eleitor.

    Returns:
        bool: True se registrado com sucesso, False se falhar.
    """
    connection, cursor = get_cursor()

    try:
        encrypted_protocol = encrypt_hill_cipher(protocol)
        date_vote = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO votacao (protocolo_criptografado, id_candidato, data_voto)
            VALUES (%s, %s, %s)
        """, (encrypted_protocol, candidate_id, date_vote))

        cursor.execute("""
            UPDATE eleitores
            SET status_votacao = TRUE
            WHERE titulo_eleitor = %s
        """, (voter_id,))

        connection.commit()
        return True

    except Exception as e:
        connection.rollback()
        print("Erro ao registrar voto:", e)
        return False

    finally:
        cursor.close()
        connection.close()



def cast_vote():
    """
    Executa o fluxo completo de votação de um eleitor.

    Fluxo:
    1. Identifica o eleitor pelas credenciais
    2. Verifica se já votou
    3. Captura o número do candidato com confirmação
    4. Gera o protocolo
    5. Registra o voto no banco
    6. Exibe o protocolo e grava nos logs

    Args:
        None

    Returns:
        None
    """
    # IDENTIFICAÇÃO DO ELEITOR
    voter_id = input("Título de eleitor: ")
    cpf_partial = input("4 primeiros dígitos do CPF: ")
    access_key = input("Chave de acesso: ")

    voter = identify_voter(voter_id, cpf_partial, access_key)

    # Eleitor não encontrado
    if voter is None:
        print("Dados inválidos! Acesso negado.")
        register_access_denied_log()
        return

    # Eleitor já votou
    if voter["status_votacao"]:
        print("Este eleitor já realizou o voto!")
        register_double_vote_log()
        return

    # ESCOLHA DO CANDIDATO
    candidate_id = None
    candidate_number = None
    confirmed = False

    while not confirmed:
        number = input("Digite o número do candidato: ")
        candidate = get_candidate_by_number(number)

        if candidate:
            print(f"\nCandidato: {candidate['nome']}")
            print(f"Número:    {candidate['numero_de_votacao']}")
            print(f"Partido:   {candidate['partido']}")
            candidate_id = candidate["id"]
            candidate_number = candidate["numero_de_votacao"]
        else:
            print("Candidato não encontrado. O voto será registrado como NULO.")
            candidate_id = None
            candidate_number = None

        confirm = input("\nConfirma o voto? (Sim/Não): ").strip()

        if confirm == "Sim":
            break
        else:
            print("Voto cancelado. Digite novamente.\n")

    # GERAÇÃO DO PROTOCOLO
    protocol = generate_voting_protocol(candidate_number)

    # REGISTRO NO BANCO 
    success = register_vote(voter_id, candidate_id, protocol)

    if success:
        # Exibe protocolo original para o eleitor
        print(f"\nVoto confirmado!")
        print(f"Guarde seu protocolo: {protocol}")

        # Grava logs e protocolo no arquivo
        register_vote_success_log()
        register_protocol(protocol)
    else:
        print("Erro ao registrar o voto. Tente novamente.")