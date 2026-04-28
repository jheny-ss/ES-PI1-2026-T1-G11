from cpf_validation import validate_cpf

# =========================
# TESTANDO FUNÇÃO
# EXECUTE NO TERMINAL: python models/validators/cpf_validation.py
# =========================

# =========================
# CPFs VÁLIDOS - DEVE RETORNAR 6 TRUES
# =========================

print(validate_cpf("52998224725"))
print(validate_cpf("11144477735"))
print(validate_cpf("12345678909"))
print(validate_cpf("93541134780"))
print(validate_cpf("39053344705"))
print(validate_cpf("529.982.247-25"))

# =========================
# CPFs INVÁLIDOS - DEVE RETORNAR 6 FALSES
# =========================

print(validate_cpf("52998224724")) # dígito errado
print(validate_cpf("11144477734")) # dígito errado
print(validate_cpf("00000000000")) # todos iguais
print(validate_cpf("123")) # tamanho inválido
print(validate_cpf("abc12345678")) # letras
print(validate_cpf("...........")) # pontos
