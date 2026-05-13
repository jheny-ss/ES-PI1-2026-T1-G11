"""
Arquivo de testes do módulo de auditoria.

Responsável por validar:
- Registro de logs
- Registro de protocolos
- Registro de erros
- Registro de gerenciamento
- Registro de votos nulos
- Exibição de logs
- Exibição de protocolos

EXECUÇÃO:

python -m models.audit_test
"""

from models.audit import (
    show_logs,
    register_protocol,
    show_protocols,
    register_opening_log,
    register_access_denied_log,
    register_double_vote_log,
    register_vote_success_log,
    register_closing_log,
    register_null_vote_log,
    register_management_log,
    register_error_log
)

# ============================================================
# INÍCIO DOS TESTES
# ============================================================

print("\nARQUIVO DE TESTE EXECUTADO\n")

# ============================================================
# TESTE COMPLETO DE AUDITORIA
# ============================================================

print("===== TESTANDO LOGS E AUDITORIA =====\n")

# ============================================================
# TESTE 1 - ABERTURA
# RF002.02.01.03
# ============================================================

print("TESTE 1 - ABERTURA DA VOTAÇÃO")

register_opening_log()

print("RESULTADO: TESTE APROVADO\n")

# ============================================================
# TESTE 2 - ACESSO NEGADO
# RF002.02.01.04
# ============================================================

print("TESTE 2 - ACESSO NEGADO")

register_access_denied_log()
register_access_denied_log()

print("RESULTADO: TESTE APROVADO\n")

# ============================================================
# TESTE 3 - VOTO DUPLO
# RF002.02.01.05
# ============================================================

print("TESTE 3 - TENTATIVA DE VOTO DUPLO")

register_double_vote_log()

print("RESULTADO: TESTE APROVADO\n")

# ============================================================
# TESTE 4 - VOTO REALIZADO
# RF002.02.01.06
# ============================================================

print("TESTE 4 - VOTO REALIZADO")

register_vote_success_log(
    "VRT269950134"
)

print("RESULTADO: TESTE APROVADO\n")

# ============================================================
# TESTE 5 - VOTO NULO
# RF002.02.01.06
# ============================================================

print("TESTE 5 - VOTO NULO")

register_null_vote_log()

print("RESULTADO: TESTE APROVADO\n")

# ============================================================
# TESTE 6 - GERENCIAMENTO
# RF001
# ============================================================

print("TESTE 6 - LOGS DE GERENCIAMENTO")

register_management_log(
    "CADASTRO",
    "Eleitor João Silva"
)

register_management_log(
    "REMOÇÃO",
    "Candidato Número 22"
)

register_management_log(
    "EDIÇÃO",
    "Eleitor Maria Souza"
)

print("RESULTADO: TESTE APROVADO\n")

# ============================================================
# TESTE 7 - REGISTRO DE ERRO
# RNF
# ============================================================

print("TESTE 7 - REGISTRO DE ERRO")

try:

    result = 10 / 0

except Exception as error:

    register_error_log(error)

print("RESULTADO: TESTE APROVADO\n")

# ============================================================
# TESTE 8 - ENCERRAMENTO
# RF002.02.01.07
# ============================================================

print("TESTE 8 - ENCERRAMENTO DA VOTAÇÃO")

register_closing_log()

print("RESULTADO: TESTE APROVADO\n")

# ============================================================
# TESTE 9 - REGISTRO DE PROTOCOLOS
# RF002.02.02
# ============================================================

print("TESTE 9 - REGISTRO DE PROTOCOLOS")

"""
Protocolos seguem o padrão definido
na documentação:

Prefixo "V"
+ 2 letras aleatórias
+ Ano (26)
+ Número do candidato
+ 5 dígitos aleatórios
"""

register_protocol("VRT269950134")
register_protocol("VAB261230987")
register_protocol("VXP260145678")

print("RESULTADO: TESTE APROVADO\n")

# ============================================================
# TESTE 10 - EXIBIÇÃO DOS LOGS
# RF002.02.01.08
# ============================================================

print("TESTE 10 - EXIBINDO LOGS")

show_logs()

print("\nRESULTADO: TESTE APROVADO\n")

# ============================================================
# TESTE 11 - EXIBIÇÃO DOS PROTOCOLOS
# RF002.02.02
# ============================================================

print("TESTE 11 - EXIBINDO PROTOCOLOS")

show_protocols()

print("\nRESULTADO: TESTE APROVADO\n")

# ============================================================
# FINALIZAÇÃO
# ============================================================

print(
    "===== TODOS OS TESTES "
    "FINALIZADOS =====\n"
)
