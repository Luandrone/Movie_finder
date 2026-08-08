from app.api import buscar_filme,buscar_detalhes
from app.formatador import mostrar_resultado
from app.menu import selecionar_filme

lista_de_filmes = buscar_filme('batman')

mostrar_resultado(lista_de_filmes)
filme = selecionar_filme(lista_de_filmes)
buscar_detalhes(filme)
print(filme)

