from app.api import buscar_filme, buscar_detalhes, buscar_disponibilidade
from app.formatador import mostrar_resultado, mostrar_filme
from app.menu import selecionar_filme
from app.excecoes import ErroApi
from app.banco.repositorio import salvar_filme, buscar_filmes_banco, buscar_disponibilidades_do_filme_no_banco, \
    buscar_generos_do_filme_no_banco


def buscar_e_mostrar_filme():

    nome_do_filme = input('Digite o nome do filme: ')
    try:
        lista_de_filmes = buscar_filme(nome_do_filme)

        if lista_de_filmes:

            mostrar_resultado(lista_de_filmes)

            filme = selecionar_filme(lista_de_filmes)

            buscar_detalhes(filme)

            buscar_disponibilidade(filme)

            resultado = salvar_filme(filme)
            if resultado['status'] == 'atualizado':
                print(f'Filme atualizado no banco com sucesso!')
            elif resultado['status'] == 'já_existe':
                print('Não houve mudança no banco!')
            elif resultado['status'] == 'novo':
                print('Filme salvo no banco com sucesso!')

            mostrar_filme(filme)

        else:
            print('Nenhum filme encontrado!')

    except ErroApi as erro:
        if erro.tipo == 'Problema de conexão':
            print('Não foi possível conectar à API.')

        elif erro.tipo == 'Problema de Http':
            print('A API retornou um erro.')

        else:
            print('Algum problema ocorreu!')
        return

def exibir_filmes_do_banco():

    filmes = buscar_filmes_banco()

    if filmes:
        mostrar_resultado(filmes)
        filme = selecionar_filme(filmes)
        filme.disponibilidade = buscar_disponibilidades_do_filme_no_banco(filme)
        filme.generos = buscar_generos_do_filme_no_banco(filme)
        mostrar_filme(filme)
    else:
        print('Não existe nenhum filme salvo atualmente')



