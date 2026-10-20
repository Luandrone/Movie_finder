# Casos de uso que conectam entrada, API, persistência e apresentação.
from app.api import buscar_filme, buscar_detalhes, buscar_disponibilidade
from app.formatador import mostrar_resultado, mostrar_filme
from app.menu import selecionar_filme
from app.excecoes import ErroApi
from app.banco.repositorio import salvar_filme, buscar_filmes_banco, buscar_disponibilidades_do_filme_no_banco, \
    buscar_generos_do_filme_no_banco, excluir_filme_banco, atualizar_favorito_banco, buscar_filmes_favoritos_banco

def _salvar_filme_se_confirmado(filme):
    resposta = input('Deseja salvar o filme ? (S/N): ').strip().lower()

    if resposta != 's':
        print('Filme não foi salvo.')
        return

    resultado = salvar_filme(filme)

    if resultado['status'] == 'atualizado':
        print('Filme atualizado no banco com sucesso!')
    elif resultado['status'] == 'já_existe':
        print('Não houve mudança no banco!')
    elif resultado['status'] == 'novo':
        print('Filme salvo no banco com sucesso!')

def buscar_e_mostrar_filme():
    # Fluxo de busca: procurar, selecionar, completar, salvar e exibir um filme.

    nome_do_filme = input('Digite o nome do filme: ')
    try:
        lista_de_filmes = buscar_filme(nome_do_filme)

        if not lista_de_filmes:
            print('Nenhum filme encontrado!')
            return

        mostrar_resultado(lista_de_filmes)
        filme = selecionar_filme(lista_de_filmes)

        buscar_detalhes(filme)
        buscar_disponibilidade(filme)
        mostrar_filme(filme)

        _salvar_filme_se_confirmado(filme)


    except ErroApi as erro:
        mensagens_erro = {
            'Problema de conexão': 'Não foi possível conectar à API.',
            'Problema de Http': 'A API retornou um erro.',
        }

        mensagem = mensagens_erro.get(
            erro.tipo,
            'Algum problema ocorreu!'
        )

        print(mensagem)
        return

def _completar_dados_filme_salvo(filme):
    filme.disponibilidade = buscar_disponibilidades_do_filme_no_banco(filme)
    filme.generos = buscar_generos_do_filme_no_banco(filme)
    return filme


def exibir_filmes_do_banco():
    # Fluxo local: carrega o filme salvo e suas relações para exibição.

    filmes = buscar_filmes_banco()

    if filmes:
        mostrar_resultado(filmes)
        filme = selecionar_filme(filmes)
        filme = _completar_dados_filme_salvo(filme)
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

def gerenciar_favoritos():
    filmes = buscar_filmes_banco()

    if not filmes:
        print('Não existem filmes salvos para gerenciar.')
        return

    mostrar_resultado(filmes)
    filme = selecionar_filme(filmes)

    if filme.favorito:
        print(f'O filme {filme.titulo} já está adicionado aos favoritos.')
        confirmacao = input('Você deseja remover esse filme dos favoritos ? (S/N): ').strip().lower()

    else:
        print(f'O filme {filme.titulo} ainda não está nos favoritos.')
        confirmacao = input('Você gostaria de adicionar esse filme aos favoritos ? (S/N): ').strip().lower()

    if confirmacao != 's':
        print('O filme não foi alterado.')
        return

    atualizar_favorito_banco(filme, not filme.favorito)

    if filme.favorito:
        print('Filme foi adicionado aos favoritos com sucesso!')

    else:
        print('Filme foi removido dos favoritos com sucesso!')


def exibir_filmes_favoritos():
    filmes = buscar_filmes_favoritos_banco()

    if filmes:
        mostrar_resultado(filmes)
        filme = selecionar_filme(filmes)
        filme = _completar_dados_filme_salvo(filme)
        mostrar_filme(filme)
    else:
        print('Não existe nenhum filme favorito no momento.')
