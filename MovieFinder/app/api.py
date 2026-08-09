from app.config import BASE_URL, API_KEY, MOVIE_SEARCH_ENDPOINT, MOVIE_DETAILS_ENDPOINT
import requests
from app.excecoes import ErroApi
from app.filme import Filme


# irá realizar a busca de um filme
def buscar_filme(nome_filme):
    """
    Responsabilidade:
        Pesquisar um filme na API TMDB.

    Entrada:
        Nome do filme informado pelo usuário.

    Processamento:
        Realiza uma requisição HTTP.
        Recebe o JSON da API.
        Converte cada resultado em um objeto Filme.

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

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
    }
    try:
        response = requests.get(BASE_URL + MOVIE_SEARCH_ENDPOINT, params=parametros, headers=headers)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as erro:
        raise ErroApi(erro, 'Problema de conexão')
    except requests.exceptions.HTTPError as erro:
        raise ErroApi(erro, 'Problema de Http')
    dados = response.json()
    lista_filmes = []
    for filme in dados['results']:
        objeto_filme = Filme(filme['title'], filme['release_date'][:4], filme['vote_average'], filme['id'])
        lista_filmes.append(objeto_filme)
    return lista_filmes

def buscar_detalhes(filme):

    parametros = {
        "language": "pt-BR",
    }

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
    }

    response = requests.get(f'{BASE_URL}{MOVIE_DETAILS_ENDPOINT}{filme.id}', params=parametros, headers=headers)
    dados = response.json()
    filme.sinopse = dados['overview']
    filme.duracao = dados['runtime']
    filme.poster = dados['poster_path']

    for genero in dados['genres']:
        filme.generos.append(genero['name'])






