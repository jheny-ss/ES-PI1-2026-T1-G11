def validate_cpf(cpf):
    """
    Valida matematicamente um CPF.

    Regras:
    - Deve possuir 11 dígitos numéricos.
    - Não pode possuir todos os dígitos iguais.
    - Deve possuir dígitos verificadores válidos.

    Args:
        cpf (str): CPF informado pelo usuário.

    Returns:
        bool:
            True  -> CPF válido
            False -> CPF inválido
    """

    # Remove pontos e traços
    cpf = cpf.replace(".", "").replace("-", "").strip()

    # Verifica se possui apenas números
    if not cpf.isdigit():
        return False

    # Verifica tamanho
    if len(cpf) != 11:
        return False

    # Impede CPFs com todos os números iguais
    if cpf == cpf[0] * 11:
        return False

    # =========================
    # PRIMEIRO DÍGITO VERIFICADOR
    # =========================

    total = 0
    multiplier = 10

    for digit in cpf[:9]:
        total += int(digit) * multiplier
        multiplier -= 1

    remainder = total % 11

    if remainder < 2:
        first_digit = 0
    else:
        first_digit = 11 - remainder

    # =========================
    # SEGUNDO DÍGITO VERIFICADOR
    # =========================

    total = 0
    multiplier = 11

    for digit in cpf[:10]:
        total += int(digit) * multiplier
        multiplier -= 1

    remainder = total % 11

    if remainder < 2:
        second_digit = 0
    else:
        second_digit = 11 - remainder

    # =========================
    # VALIDAÇÃO FINAL
    # =========================

    if (
        int(cpf[9]) == first_digit
        and int(cpf[10]) == second_digit
    ):
        return True

    return False

