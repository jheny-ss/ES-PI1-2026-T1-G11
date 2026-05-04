from datetime import datetime
import os


# ============================================================
# CONFIGURAÇÃO DOS ARQUIVOS
# ============================================================

"""
Diretório responsável por armazenar todos os arquivos
de auditoria do sistema.
"""
LOG_DIRECTORY = "logs"

"""
Arquivo responsável por armazenar os logs de ocorrências
do sistema de votação.
"""
LOG_FILE = f"{LOG_DIRECTORY}/system_logs.txt"

"""
Arquivo responsável por armazenar os protocolos
gerados durante o processo de votação.
"""
PROTOCOL_FILE = f"{LOG_DIRECTORY}/voting_protocols.txt"


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

    Exemplo:
        register_log(
            "ABERTURA: Votação iniciada com sucesso. Total de votos zerado."
        )
    """

    # Obtém data e hora atual do sistema
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Abre o arquivo em modo APPEND
    # "a" adiciona conteúdo sem apagar o anterior
    with open(LOG_FILE, "a", encoding="utf-8") as file:

        # Escreve o log formatado
        file.write(f"[{current_date}] {message}\n")


# ============================================================
# EVENTOS ESPECÍFICOS DE AUDITORIA
# ============================================================

def register_opening_log():
    """
    Registra oficialmente a abertura da votação.

    Deve ser executado após:
    - validação do mesário
    - realização da zerésima
    """

    register_log(
        "ABERTURA: Votação iniciada com sucesso. Total de votos zerado."
    )


def register_access_denied_log():
    """
    Registra tentativa de acesso negado.

    Deve ser executado quando:
    - mesário falhar autenticação
    - eleitor falhar identificação
    """

    register_log(
        "ALERTA: Tentativa de acesso negado."
    )


def register_double_vote_log():
    """
    Registra tentativa de voto duplo.

    Deve ser executado quando:
    - eleitor já possuir status_votacao = TRUE
    """

    register_log(
        "ALERTA: Tentativa de voto duplo."
    )


def register_vote_success_log():
    """
    Registra voto realizado com sucesso.

    Deve ser executado imediatamente após
    a confirmação do voto na urna.
    """

    register_log(
        "SUCESSO: Voto realizado com sucesso."
    )


def register_closing_log():
    """
    Registra encerramento oficial da votação.

    Deve ser executado após:
    - fechamento realizado pelo mesário
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
    """

    try:

        # Abre o arquivo em modo leitura
        with open(LOG_FILE, "r", encoding="utf-8") as file:

            # Lê todas as linhas do arquivo
            logs = file.readlines()

            # Verifica se existem logs
            if not logs:
                print("Nenhum log encontrado!")
                return

            print("\n===== LOGS DO SISTEMA =====\n")

            # Exibe cada log individualmente
            for log in logs:
                print(log.strip())

    except FileNotFoundError:
        print("Arquivo de logs não encontrado!")


# ============================================================
# REGISTRO DE PROTOCOLOS
# ============================================================

def register_protocol(protocol):
    """
    Registra um protocolo de votação.

    O protocolo funciona como um comprovante
    oficial de que o voto foi computado.

    Args:
        protocol (str):
            Código do protocolo gerado na votação.

    Exemplo:
        register_protocol("ABCD1234")
    """

    with open(PROTOCOL_FILE, "a", encoding="utf-8") as file:
        file.write(f"{protocol}\n")


# ============================================================
# EXIBIÇÃO DOS PROTOCOLOS
# ============================================================

def show_protocols():
    """
    Exibe todos os protocolos registrados.

    Funcionamento:
    - Lê todos os protocolos salvos
    - Ordena alfabeticamente
    - Exibe na tela
    """

    try:

        # Abre arquivo em modo leitura
        with open(PROTOCOL_FILE, "r", encoding="utf-8") as file:

            # Lê protocolos
            protocols = file.readlines()

            # Verifica se existem protocolos
            if not protocols:
                print("Nenhum protocolo encontrado!")
                return

            # Remove quebras de linha
            protocols = [
                protocol.strip()
                for protocol in protocols
            ]

            # Ordena alfabeticamente
            protocols.sort()

            print("\n===== PROTOCOLOS DE VOTAÇÃO =====\n")

            # Exibe protocolos
            for protocol in protocols:
                print(protocol)

    except FileNotFoundError:
        print("Arquivo de protocolos não encontrado!")
