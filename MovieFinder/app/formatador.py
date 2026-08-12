

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

    if filme.disponibilidade:

        servicos = {
            'flatrate': 'Disponível por assinatura',
            'rent': 'Disponível para alugar',
            'buy': 'Disponível para comprar',
        }

        for categoria in servicos:

            if filme.disponibilidade.get(categoria):
                encontrou_categoria = True
                print(servicos[categoria])

                for item in filme.disponibilidade[categoria]:
                    print(f'-{item["provider_name"]}')

    if not encontrou_categoria:
        print('Filme indisponível')


