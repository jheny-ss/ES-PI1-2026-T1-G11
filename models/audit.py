from datetime import datetime
import os

from models.crypto.encrypt import encrypt_hill_cipher
from models.crypto.decrypt import decrypt_hill_cipher


# ============================================================
# CONFIGURAÇÃO DOS ARQUIVOS
# ============================================================

"""
Diretório responsável por armazenar todos os arquivos
de auditoria do sistema.
"""
LOG_DIRECTORY = os.path.join("logs")

"""
Arquivo responsável por armazenar os logs de ocorrências
do sistema de votação.
"""
LOG_FILE = os.path.join(
    LOG_DIRECTORY,
    "system_logs.txt"
)

"""
Arquivo responsável por armazenar os protocolos
gerados durante o processo de votação.
"""
PROTOCOL_FILE = os.path.join(
    LOG_DIRECTORY,
    "voting_protocols.txt"
)


# ============================================================
# CRIAÇÃO AUTOMÁTICA DO DIRETÓRIO
# ============================================================

"""
Cria automaticamente o diretório de logs caso ele
não exista no projeto.

Evita erros ao tentar criar arquivos dentro de uma
pasta inexistente.
"""
os.makedirs(LOG_DIRECTORY, exist_ok=True)


# ============================================================
# REGISTRO DE LOGS
# ============================================================

def register_log(message):
    """
    Registra uma ocorrência crítica no arquivo de logs.

    O sistema adiciona automaticamente:
    - Data
    - Hora
    - Mensagem da ocorrência

    O padrão segue o requisito funcional:

    [YYYY-MM-DD HH:MM:SS] DESCRIÇÃO

    Args:
        message (str):
            Mensagem da ocorrência que será registrada.

    Returns:
        None

    Exemplo:
        register_log(
            "ABERTURA: Votação iniciada com sucesso. "
            "Total de votos zerado."
        )
    """

    # Obtém data e hora atual do sistema
    current_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Abre o arquivo em modo append
    with open(LOG_FILE, "a", encoding="utf-8") as file:

        # Escreve o log formatado
        file.write(
            f"[{current_date}] {message}\n"
        )


# ============================================================
# EVENTOS ESPECÍFICOS DE AUDITORIA
# ============================================================

def register_opening_log():
    """
    Registra oficialmente a abertura da votação.

    Deve ser executado após:
    - validação do mesário
    - realização da zerézima

    Args:
        None

    Returns:
        None
    """

    register_log(
        "ABERTURA: Votação iniciada com sucesso. "
        "Total de votos zerado."
    )


def register_access_denied_log():
    """
    Registra tentativa de acesso negado.

    Deve ser executado quando:
    - mesário falhar autenticação
    - eleitor falhar identificação

    Args:
        None

    Returns:
        None
    """

    register_log(
        "ALERTA: Tentativa de acesso negado."
    )


def register_double_vote_log():
    """
    Registra tentativa de voto duplo.

    Deve ser executado quando:
    - eleitor já possuir status_votacao = TRUE

    Args:
        None

    Returns:
        None
    """

    register_log(
        "ALERTA: Tentativa de voto duplo."
    )


def register_vote_success_log():
    """
    Registra voto realizado com sucesso.

    Deve ser executado imediatamente após
    a confirmação do voto na urna.

    Args:
        None

    Returns:
        None
    """

    register_log(
        "SUCESSO: Voto realizado com sucesso."
    )


def register_closing_log():
    """
    Registra encerramento oficial da votação.

    Deve ser executado após:
    - fechamento realizado pelo mesário

    Args:
        None

    Returns:
        None
    """

    register_log(
        "ENCERRAMENTO: Votação finalizada com sucesso."
    )


# ============================================================
# EXIBIÇÃO DOS LOGS
# ============================================================

def show_logs():
    """
    Exibe todos os logs registrados no sistema.

    Funcionamento:
    - Lê o arquivo de logs
    - Exibe todas as ocorrências registradas
    - Mantém a ordem cronológica

    Args:
        None

    Returns:
        None
    """

    try:

        # Abre arquivo em modo leitura
        with open(LOG_FILE, "r", encoding="utf-8") as file:

            # Lê todas as linhas
            logs = file.readlines()

            # Verifica se existem logs
            if not logs:
                print("Nenhum log encontrado!")
                return

            print("\n===== LOGS DO SISTEMA =====\n")

            # Exibe logs
            for log in logs:
                print(log.strip())

    except FileNotFoundError:
        print("Arquivo de logs não encontrado!")


# ============================================================
# REGISTRO DE PROTOCOLOS
# ============================================================

def register_protocol(protocol):
    """
    Registra um protocolo de votação criptografado.

    O protocolo funciona como um comprovante
    oficial de que o voto foi computado.

    Antes do armazenamento, o protocolo é
    criptografado utilizando a Cifra de Hill,
    conforme exigido no RNF006.

    Args:
        protocol (str):
            Código do protocolo gerado na votação.

    Returns:
        None

    Exemplo:
        register_protocol("VRT269950134")
    """

    # Criptografa protocolo
    encrypted_protocol = encrypt_hill_cipher(
        protocol
    )

    # Salva protocolo criptografado
    with open(
        PROTOCOL_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            f"{encrypted_protocol}\n"
        )


# ============================================================
# EXIBIÇÃO DOS PROTOCOLOS
# ============================================================

def show_protocols():
    """
    Exibe todos os protocolos registrados.

    Funcionamento:
    - Lê protocolos criptografados
    - Descriptografa os dados
    - Ordena alfabeticamente
    - Exibe no terminal

    Args:
        None

    Returns:
        None
    """

    try:

        # Abre arquivo em modo leitura
        with open(
            PROTOCOL_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            # Lê protocolos
            protocols = file.readlines()

            # Verifica se existem protocolos
            if not protocols:
                print("Nenhum protocolo encontrado!")
                return

            # Remove quebra de linha
            protocols = [
                protocol.strip()
                for protocol in protocols
            ]

            # Descriptografa protocolos
            decrypted_protocols = []

            for protocol in protocols:

                decrypted_protocol = (
                    decrypt_hill_cipher(protocol)
                )

                decrypted_protocols.append(
                    decrypted_protocol
                )

            # Ordena alfabeticamente
            decrypted_protocols.sort()

            print(
                "\n===== PROTOCOLOS DE VOTAÇÃO =====\n"
            )

            # Exibe protocolos
            for protocol in decrypted_protocols:
                print(protocol)

    except FileNotFoundError:
        print(
            "Arquivo de protocolos não encontrado!"
        )
