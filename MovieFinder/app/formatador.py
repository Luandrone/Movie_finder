

def mostrar_resultado(lista_de_filmes):
    print('RESULTADO')
    for indice,filme in enumerate(lista_de_filmes):
        print(f'{indice + 1} - {filme.titulo}')

def mostrar_filme(filme):
    print(
        f'Filme: {filme.titulo}\n'
        f'Ano: {filme.ano}\n'
        f'Nota: {filme.nota}\n'
        f'Duração: {filme.duracao}\n'
        f'Sinopse: {filme.sinopse}\n'
        f'Gênero: {', '.join(filme.generos)}\n')

    mostrar_disponibilidade(filme)

def mostrar_disponibilidade(filme):

    encontrou_categoria = False

    for disponibilidade in filme.disponibilidade:
        if disponibilidade['tipo'] == 'buy':
            encontrou_categoria = True
            print(f'Disponível para comprar \n'
                  f'- {disponibilidade["provider_name"]}\n')
        elif disponibilidade['tipo'] == 'rent':
            encontrou_categoria = True
            print(f'Disponível para alugar \n'
                  f'- {disponibilidade["provider_name"]}\n')
        elif disponibilidade['tipo'] == 'flatrate':
            encontrou_categoria = True
            print(f'Disponível por assinatura \n'
                  f'- {disponibilidade["provider_name"]}\n')

    if not encontrou_categoria:
        print('Filme indisponível')


