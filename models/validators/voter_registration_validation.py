def registration_validation(registration_card):
    if not registration_card.isdigit():  # Verifica se o título contém apenas números reais
        return False
    if len(registration_card) != 12:
        return False
    
    n_sequence = registration_card[:8]
    uf = registration_card[8:10]
    dv1p = int(registration_card[10])
    dv2p = int(registration_card[11])
    sum1 = 0
    weight = [2, 3, 4, 5, 6, 7, 8, 9]
    
    for i in range(8):
        sum1 += int(n_sequence[i]) * weight[i]
    
    rest = sum1 % 11
    dv1 = 0 if rest >= 10 else rest

    if uf in ["01", "02"]:
        if rest == 10 or rest == 0:
            dv1 = 1 if rest == 0 else 0 

    sum2 = (int(uf[0]) * 7) + (int(uf[1]) * 8) + (dv1 * 9)
    rest2 = sum2 % 11
    dv2 = 0 if rest2 >= 10 else rest2
    
    if uf in ["01", "02"]:
        if rest2 == 10 or rest2 == 0:
            dv2 = 1 if rest2 == 0 else 0

    return dv1p == dv1 and dv2p == dv2