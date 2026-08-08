from app.api import buscar_filme,buscar_detalhes
lista_de_filmes = buscar_filme('batman')

def mostrar_resultado(lista_de_filmes):
    print('RESULTADO')
    for indice,filme in enumerate(lista_de_filmes):
        print(f'{indice + 1} - {filme.titulo}')

def selecionar_filme(lista_de_filmes):
    numero_filme = int(input('Digite o numero do filme: '))
    numero_filme -= 1
    return lista_de_filmes[numero_filme]

mostrar_resultado(lista_de_filmes)
filme = selecionar_filme(lista_de_filmes)
print(filme.titulo)
buscar_detalhes(filme)
print(filme)

