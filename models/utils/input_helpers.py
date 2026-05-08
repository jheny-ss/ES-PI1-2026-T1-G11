def input_with_exit(
    message,
    validation_function,
    error_message="Entrada inválida!"
):
    """
    Solicita uma entrada validada ao usuário.

    Permite cancelar digitando 0.

    Args:
        message (str):
            Mensagem exibida.

        validation_function (function):
            Função de validação.

        error_message (str):
            Mensagem de erro.

    Returns:
        str | None:
            Valor validado ou None.
    """

    value = input(f"{message} (0 para voltar): ")

    while not validation_function(value):

        if value == "0":
            return None

        print(error_message)

        value = input(
            f"{message} (0 para voltar): "
        )

    return value


def input_yes_no(message):
    """
    Solicita resposta Sim/Não.

    Permite cancelar digitando 0.

    Args:
        message (str):
            Pergunta exibida.

    Returns:
        bool | None:
            True para Sim,
            False para Não,
            None para cancelar.
    """

    value = input(
        f"{message} (Sim/Não | 0 para voltar): "
    )

    while value not in [
        "Sim",
        "Não",
        "0"
    ]:

        print("Entrada inválida!")

        value = input(
            f"{message} "
            "(Sim/Não | 0 para voltar): "
        )

    if value == "0":
        return None

    return value == "Sim"
