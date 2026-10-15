# Ponto de entrada: mantém o menu ativo e encaminha as opções aos casos de uso.
from app.serviço import exibir_filmes_do_banco
from app.menu import mostrar_menu
from app.serviço import buscar_e_mostrar_filme

while True:

    opcao = mostrar_menu()

    if opcao == 1:
        buscar_e_mostrar_filme()

    elif opcao == 2:
        exibir_filmes_do_banco()

    elif opcao == 3:
        break


