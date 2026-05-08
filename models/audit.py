from datetime import datetime
import os

from models.crypto.encrypt import encrypt_hill_cipher
from models.crypto.decrypt import decrypt_hill_cipher

# ============================================================
# CONFIGURAÇÃO DOS ARQUIVOS
# ============================================================

"""
Diretório responsável por armazenar
os arquivos de auditoria do sistema.
"""
LOG_DIRECTORY = os.path.join("logs")

"""
Arquivo responsável por armazenar
os logs do sistema.
"""
LOG_FILE = os.path.join(
    LOG_DIRECTORY,
    "system_logs.txt"
)

"""
Arquivo responsável por armazenar
os protocolos de votação.
"""
PROTOCOL_FILE = os.path.join(
    LOG_DIRECTORY,
    "voting_protocols.txt"
)

# ============================================================
# CRIAÇÃO AUTOMÁTICA DO DIRETÓRIO
# ============================================================

os.makedirs(LOG_DIRECTORY, exist_ok=True)

# ============================================================
# REGISTRO DE LOGS
# ============================================================

def register_log(message):
    """
    Registra uma ocorrência no arquivo de logs.

    Args:
        message (str):
            Mensagem que será registrada.

    Returns:
        None
    """

    current_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            f"[{current_date}] {message}\n"
        )


# ============================================================
# EVENTOS DE AUDITORIA
# ============================================================

def register_opening_log():
    """
    Registra abertura da votação.

    Returns:
        None
    """

    register_log(
        "ABERTURA: Votação iniciada com sucesso."
    )


def register_closing_log():
    """
    Registra encerramento da votação.

    Returns:
        None
    """

    register_log(
        "ENCERRAMENTO: Votação finalizada com sucesso."
    )


def register_access_denied_log():
    """
    Registra tentativa de acesso negado.

    Returns:
        None
    """

    register_log(
        "ALERTA: Tentativa de acesso negado."
    )


def register_double_vote_log():
    """
    Registra tentativa de voto duplo.

    Returns:
        None
    """

    register_log(
        "ALERTA: Tentativa de voto duplo."
    )


def register_vote_success_log(protocol):
    """
    Registra voto realizado com sucesso.

    Args:
        protocol (str):
            Protocolo do voto.

    Returns:
        None
    """

    register_log(
        f"SUCESSO: Voto registrado. "
        f"Protocolo: {protocol}"
    )


def register_null_vote_log():
    """
    Registra voto nulo.

    Returns:
        None
    """

    register_log(
        "SUCESSO: Voto nulo registrado."
    )


def register_management_log(action, entity):
    """
    Registra ações administrativas.

    Args:
        action (str):
            Ação executada.

        entity (str):
            Entidade afetada.

    Returns:
        None
    """

    register_log(
        f"GERENCIAMENTO: {action} -> {entity}"
    )


def register_error_log(error):
    """
    Registra erros internos do sistema.

    Args:
        error (Exception | str):
            Erro capturado.

    Returns:
        None
    """

    register_log(
        f"ERRO: {str(error)}"
    )

# ============================================================
# EXIBIÇÃO DOS LOGS
# ============================================================

def show_logs():
    """
    Exibe todos os logs registrados.

    Returns:
        None
    """

    try:

        with open(
            LOG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            logs = file.readlines()

            if not logs:

                print(
                    "Nenhum log encontrado!"
                )

                return

            print(
                "\n===== LOGS DO SISTEMA =====\n"
            )

            for log in logs:
                print(log.strip())

    except FileNotFoundError:

        print(
            "Arquivo de logs não encontrado!"
        )

# ============================================================
# PROTOCOLOS
# ============================================================

def register_protocol(protocol):
    """
    Registra protocolo criptografado.

    Args:
        protocol (str):
            Protocolo original.

    Returns:
        None
    """

    encrypted_protocol = encrypt_hill_cipher(
        protocol
    )

    with open(
        PROTOCOL_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            f"{encrypted_protocol}\n"
        )


def show_protocols():
    """
    Exibe protocolos descriptografados.

    Returns:
        None
    """

    try:

        with open(
            PROTOCOL_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            protocols = file.readlines()

            if not protocols:

                print(
                    "Nenhum protocolo encontrado!"
                )

                return

            protocols = [
                protocol.strip()
                for protocol in protocols
            ]

            decrypted_protocols = []

            for protocol in protocols:

                decrypted_protocol = (
                    decrypt_hill_cipher(protocol)
                )

                decrypted_protocols.append(
                    decrypted_protocol
                )

            decrypted_protocols.sort()

            print(
                "\n===== PROTOCOLOS =====\n"
            )

            for protocol in decrypted_protocols:
                print(protocol)

    except FileNotFoundError:

        print(
            "Arquivo de protocolos não encontrado!"
        )
