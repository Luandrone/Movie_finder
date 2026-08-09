from app.menu import mostrar_menu
from app.serviço import buscar_e_mostrar_filme

while True:
    try:
        opcao = mostrar_menu()

        if opcao == 1:
            buscar_e_mostrar_filme()

        elif opcao == 2:
            break

        else:
            print(f'Número {opcao} não é válido')

    except (ValueError, TypeError):
        print('Valor incorreto!')



