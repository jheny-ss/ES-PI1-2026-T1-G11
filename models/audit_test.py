from models.audit import (
    show_logs,
    register_protocol,
    show_protocols,
    register_opening_log,
    register_access_denied_log,
    register_double_vote_log,
    register_vote_success_log,
    register_closing_log
)

print("ARQUIVO DE TESTE EXECUTADO")


# =========================
# TESTE COMPLETO DE AUDITORIA
# (OPCIONAL)CRIE UM ARQUIVO DENTRO DA PASTA MODELS:
# __init__.py
# EXECUTE:
# python -m models.audit_test
# =========================


print("\n===== TESTANDO LOGS =====\n")


# =========================
# TESTE 1 - ABERTURA
# RF002.02.01.03
# =========================

print("TESTE 1 - ABERTURA DA VOTAÇÃO")

register_opening_log()


# =========================
# TESTE 2 - ACESSO NEGADO
# RF002.02.01.04
# =========================

print("TESTE 2 - ACESSO NEGADO")

register_access_denied_log()
register_access_denied_log()


# =========================
# TESTE 3 - VOTO DUPLO
# RF002.02.01.05
# =========================

print("TESTE 3 - TENTATIVA DE VOTO DUPLO")

register_double_vote_log()


# =========================
# TESTE 4 - VOTO REALIZADO
# RF002.02.01.06
# =========================

print("TESTE 4 - VOTO REALIZADO")

register_vote_success_log()


# =========================
# TESTE 5 - ENCERRAMENTO
# RF002.02.01.07
# =========================

print("TESTE 5 - ENCERRAMENTO DA VOTAÇÃO")

register_closing_log()


# =========================
# TESTE 6 - REGISTRO DE PROTOCOLOS
# RF002.02.02
# =========================

print("TESTE 6 - REGISTRO DE PROTOCOLOS")

register_protocol("PROTOCOLO-ZZZ999")
register_protocol("PROTOCOLO-AAA111")
register_protocol("PROTOCOLO-MMM555")


# =========================
# TESTE 7 - EXIBIÇÃO DOS LOGS
# RF002.02.01.08
# =========================

print("\nTESTE 7 - EXIBINDO LOGS")

show_logs()


# =========================
# TESTE 8 - EXIBIÇÃO DOS PROTOCOLOS
# RF002.02.02
# =========================

print("\nTESTE 8 - EXIBINDO PROTOCOLOS")

show_protocols()


print("\n===== TESTES FINALIZADOS =====")
