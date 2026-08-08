def mostrar_menu():
    print('=' * 25)
    print('MOVIEFINDER'.center(25))
    print('=' * 25)
    print('1 - Buscar filme')
    print('2 - Sair')
    print('=' * 25)
    opcao = int(input('Escolha uma opção: '))
    return opcao

def selecionar_filme(lista_de_filmes):
    while True:
        try:
            numero_filme = int(input('Digite o numero do filme: '))
            if numero_filme > 0:
                numero_filme -= 1
                return lista_de_filmes[numero_filme]
            else:
                print('Opção invalida! Digite novamente')
        except (ValueError, IndexError):
            print('Opção invalida! Digite novamente')


