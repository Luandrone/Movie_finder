def mostrar_resultado(lista_de_filmes):
    print('RESULTADO')
    for indice,filme in enumerate(lista_de_filmes):
        print(f'{indice + 1} - {filme.titulo}')