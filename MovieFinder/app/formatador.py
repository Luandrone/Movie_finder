


def mostrar_resultado(lista_de_filmes):
    print('RESULTADO')
    for indice,filme in enumerate(lista_de_filmes):
        print(f'{indice + 1} - {filme.titulo}')

def mostrar_filme(filme):
    generos = ', '.join(genero['nome'] for genero in filme.generos)
    print(
        f'Filme: {filme.titulo}\n'
        f'Ano: {filme.ano}\n'
        f'Nota: {filme.nota}\n'
        f'Duração: {filme.duracao}\n'
        f'Sinopse: {filme.sinopse}\n'
        f'Gênero: {generos}\n')

    mostrar_disponibilidade(filme)

def mostrar_disponibilidade(filme):

    encontrou_categoria = False
    comprar = []
    alugar = []
    assinatura = []

    for disponibilidade in filme.disponibilidade:
        if disponibilidade['tipo'] == 'buy':
            comprar.append(disponibilidade['provider_name'])
            encontrou_categoria = True

        elif disponibilidade['tipo'] == 'rent':
            alugar.append(disponibilidade['provider_name'])
            encontrou_categoria = True

        elif disponibilidade['tipo'] == 'flatrate':
            assinatura.append(disponibilidade['provider_name'])
            encontrou_categoria = True


    if comprar:
        print('Disponível para comprar')
        for provedor in comprar:
            print(f' - {provedor}')

    if alugar:
        print('Disponível para alugar')
        for provedor in alugar:
            print(f' - {provedor}')

    if assinatura:
        print('Disponível para assinatura')
        for provedor in assinatura:
            print(f' - {provedor}')


    if not encontrou_categoria:
        print('Filme indisponível')



