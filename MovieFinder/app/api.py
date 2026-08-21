from app.config import BASE_URL, MOVIE_SEARCH_ENDPOINT, MOVIE_PROVIDERS_ENDPOINT, headers, MOVIE_DETAILS_ENDPOINT
import requests
from app.excecoes import ErroApi
from app.filme import Filme
from app.transformador import transformar_filmes


def fazer_requisicao(url,cabecalho, parametros=None):
    try:
        response = requests.get(url, params=parametros, headers=cabecalho)
        response.raise_for_status()

    except requests.exceptions.ConnectionError as erro:
        raise ErroApi(erro, 'Problema de conexão')

    except requests.exceptions.HTTPError as erro:
        raise ErroApi(erro, 'Problema de Http')
    return response

# irá realizar a busca de um filme
def buscar_filme(nome_filme):
    """
    Responsabilidade:
        Pesquisar um filme na API TMDB.

    Entrada:
        Nome do filme informado pelo usuário.

    Processamento:
        Monta os parâmetros da pesquisa.
        Realiza uma requisição HTTP.
        Converte a resposta para dados Python.
        Envia os dados para transformação em objetos Filme.

    :return:
        Lista de objetos Filme.
    """

    parametros = {
        'query': nome_filme,
        'language': 'pt-BR',
        'region': 'BR',
        'page': 1,
        'include_adult': False

    }

    response = fazer_requisicao(f'{BASE_URL}{MOVIE_SEARCH_ENDPOINT}', headers, parametros)

    dados = response.json()

    lista_filmes = transformar_filmes(dados)

    return lista_filmes

def buscar_detalhes(filme):
    parametros = {
        "language": "pt-BR",
    }

    response = fazer_requisicao(f'{BASE_URL}{MOVIE_DETAILS_ENDPOINT}{filme.id}', headers, parametros)

    dados = response.json()
    filme.sinopse = dados['overview']
    filme.duracao = dados['runtime']
    filme.poster = dados['poster_path']

    for genero in dados['genres']:
        filme.generos.append(genero['name'])

def buscar_disponibilidade(filme):

    response = fazer_requisicao(f'{BASE_URL}{MOVIE_DETAILS_ENDPOINT}{filme.id}{MOVIE_PROVIDERS_ENDPOINT}',headers)

    dados = response.json()
    dados_brasil = dados['results'].get('BR')

    if dados_brasil is None:
        filme.disponibilidade = {}
    else:
        filme.disponibilidade = dados_brasil



