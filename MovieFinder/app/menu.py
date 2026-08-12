def mostrar_menu():
    print('=' * 25)
    print('MOVIEFINDER'.center(25))
    print('=' * 25)
    print('1 - Buscar filme')
    print('2 - Sair')
    print('=' * 25)
    while True:
        try:

            opcao = int(input('Escolha uma opção: '))

            if opcao in (1, 2):
                return opcao

            else:
                print(f'Número {opcao} não é válido')

        except ValueError:
            print('Valor incorreto!')




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

