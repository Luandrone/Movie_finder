from app.api import buscar_filme,buscar_detalhes
from app.formatador import mostrar_resultado
from app.menu import selecionar_filme, mostrar_menu

while True:
    opcao = mostrar_menu()

    if opcao == 1:
        nome_do_filme = str(input('Digite o nome do filme: '))
        lista_de_filmes = buscar_filme(nome_do_filme)

        mostrar_resultado(lista_de_filmes)
        filme = selecionar_filme(lista_de_filmes)
        buscar_detalhes(filme)
        print(filme)
    if opcao == 2:
        break



