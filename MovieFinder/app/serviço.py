from app.api import buscar_filme, buscar_detalhes
from app.formatador import mostrar_resultado
from app.menu import selecionar_filme


def buscar_e_mostrar_filme():
    nome_do_filme = input('Digite o nome do filme: ')
    lista_de_filmes = buscar_filme(nome_do_filme)
    if lista_de_filmes:
        mostrar_resultado(lista_de_filmes)
        filme = selecionar_filme(lista_de_filmes)
        buscar_detalhes(filme)
        print(filme)
    else:
        print('Nenhum filme encontrado!')