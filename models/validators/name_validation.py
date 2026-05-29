def validate_full_name(name):
    """
    Valida se o nome informado possui nome e sobrenome
    e contém apenas caracteres alfabéticos.

    Args:
        name (str):
            Nome completo informado pelo usuário.

    Returns:
        bool:
            True se o nome for válido.
            False caso contrário.
    """

    name = name.strip()

    # Precisa ter pelo menos duas partes (nome e sobrenome)
    parts = name.split()
    if len(parts) < 2:
        return False

    # Verifica se todas as partes têm apenas letras (sem números)
    for part in parts:
        if not part.isalpha():
            return False

    return True

