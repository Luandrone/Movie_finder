from app.menu import mostrar_menu
from app.serviço import buscar_e_mostrar_filme

while True:

    opcao = mostrar_menu()
    if opcao == 2:
        break
    buscar_e_mostrar_filme()
