def validate_full_name(name):
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