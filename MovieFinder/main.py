# Ponto de entrada: mantém o menu ativo e encaminha as opções aos casos de uso.
from app.serviço import exibir_filmes_do_banco, excluir_filme_salvo, gerenciar_favoritos, exibir_filmes_favoritos
from app.menu import mostrar_menu
from app.serviço import buscar_e_mostrar_filme

while True:

    opcao = mostrar_menu()

    if opcao == 1:
        buscar_e_mostrar_filme()

    elif opcao == 2:
        exibir_filmes_do_banco()

    elif opcao == 3:
        excluir_filme_salvo()

    elif opcao == 4:
        gerenciar_favoritos()

    elif opcao == 5:
        exibir_filmes_favoritos()

    elif opcao == 6:
        print('Até a próxima!!!')
        break

