# Casos de uso que conectam entrada, API, persistência e apresentação.
from app.api import buscar_filme, buscar_detalhes, buscar_disponibilidade
from app.formatador import mostrar_resultado, mostrar_filme
from app.menu import selecionar_filme
from app.excecoes import ErroApi
from app.banco.repositorio import salvar_filme, buscar_filmes_banco, buscar_disponibilidades_do_filme_no_banco, \
    buscar_generos_do_filme_no_banco, excluir_filme_banco


def buscar_e_mostrar_filme():
    # Fluxo de busca: procurar, selecionar, completar, salvar e exibir um filme.

    nome_do_filme = input('Digite o nome do filme: ')
    try:
        lista_de_filmes = buscar_filme(nome_do_filme)

        if lista_de_filmes:

            mostrar_resultado(lista_de_filmes)

            filme = selecionar_filme(lista_de_filmes)

            buscar_detalhes(filme)

            buscar_disponibilidade(filme)

            mostrar_filme(filme)

            resposta = input('Deseja salvar o filme ? (S/N): ').strip().lower()

            if resposta != 's':
                print('Filme não foi salvo.')
                return


            resultado = salvar_filme(filme)

            if resultado['status'] == 'atualizado':
                print(f'Filme atualizado no banco com sucesso!')
            elif resultado['status'] == 'já_existe':
                print('Não houve mudança no banco!')
            elif resultado['status'] == 'novo':
                print('Filme salvo no banco com sucesso!')

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
    # Fluxo local: carrega o filme salvo e suas relações para exibição.

    filmes = buscar_filmes_banco()

    if filmes:
        mostrar_resultado(filmes)
        filme = selecionar_filme(filmes)
        filme.disponibilidade = buscar_disponibilidades_do_filme_no_banco(filme)
        filme.generos = buscar_generos_do_filme_no_banco(filme)
        mostrar_filme(filme)
    else:
        print('Não existe nenhum filme salvo atualmente')

def excluir_filme_salvo():
    filmes = buscar_filmes_banco()

    if not filmes:
        print('Não existe nenhum filme salvo atualmente')
        return

    mostrar_resultado(filmes)
    filme = selecionar_filme(filmes)

    confirmacao = input(f'Você deseja excluir "{filme.titulo}"? (S/N): ').strip().lower()

    if confirmacao != 's':
        print('A exclusão foi cancelada!')
        return
    else:
        excluir_filme_banco(filme)
        print('Filme excluído com sucesso!')
