print("-"*50)
print("MENU".center(50))
print("-"*50)
print("\n1 - GERENCIAMENTO")
print("2 - VOTAÇÃO")
print("3 - RESULTADOS")
print("4 - AUDITORIA")
opc = int(input("\nSELECIONE UMA OPÇÃ0: "))
print("-"*50)

match opc:
    case 1:
        print("-"*50)
        print("")
        print("GERENCIAMENTO".center(50, "-"))
        print("\n1 - ELEITORES")
        print("2 - CANDIDATOS")
        opc1 = int(input("\n QUEM VOCÊ DESEJA GERENCIAR: "))
        print("-"*50)

        match opc1:
            case 1:
                print("")
                print("\nELEITORES".center(50, "-"))
            case 2:
                print("")
                print("CANDIDATOS".center(50, "-"))


    case 2:
        print("-"*50)
        print("")
        print("VOTAÇÃO".center(50, "-"))
        print("\n1 - ABRIR SISTEMA")
        print("2 - VOTAR")
        print("3 - ENCERRAR VOTAÇÃO")
        opc2 = int(input("\n O QUE VOCÊ DESEJA FAZER: "))
        print("-"*50)

        match opc2:
            case 1:
                print("")
                print("\nABRIR SISTEMA".center(50, "-"))
            case 2:
                print("")
                print("VOTAR".center(50, "-"))
            case 3:
                print("")
                print("ENCERRAR VOTAÇÃO".center(50, "-"))
    case 3: 
        print("-"*50)
        print("")
        print("RESULTADO".center(50, "-")) 
        print("\n1 - BOLETIM DE URNA")
        print("2 - ESTATÍSTICAS")
        print("3 - VOTOS POR PARTIDO")
        print("4 - VALIDAÇÃO DE INTEGRIDADE")
        opc3 = int(input("\nO QUE VOCÊ DESEJA VISUALIZAR: "))
        print("-"*50)
        match opc3:
            case 1:
                print("")
                print("BOLETIM DE URNA".center(50,"-"))
            case 2:
                print("")
                print("ESTATÍSTICAS".center(50,"-"))
            case 3:
                print("")
                print("VOTOS POR PARTIDO".center(50,"-"))
            case 4:
                print("")
                print("VALIDAÇÃO DE INTEGRIDADE".center(50,"-"))



    case 4:
        print("-"*50)
        print("\n")
        print("AUDITORIA".center(50, "-"))
        print("\n1 - LOGS DO SISTEMA")
        print("2 - PROTOCOLOS DE VOTAÇÃO")
        opc4 = int(input("\nO QUE VOCÊ DESEJA VISUALIZAR: "))
        print("-"*50)
        match opc4:
            case 1:
                print("")
                print("LOGS DO SISTEMA".center(50,"-"))
            case 2:
                print("")
                print("ROTOCOLOS DE VOTAÇÃO".center(50,"-"))