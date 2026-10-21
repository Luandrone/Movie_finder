# Integra a aplicação com o TMDB: busca, detalhes e disponibilidade.
from app.config import BASE_URL, MOVIE_SEARCH_ENDPOINT, MOVIE_PROVIDERS_ENDPOINT, headers, MOVIE_DETAILS_ENDPOINT
import requests
from app.excecoes import ErroApi
from app.filme import Filme
from app.transformador import transformar_filmes, organizar_disponibilidades


def fazer_requisicao(url,cabecalho, parametros=None):
    # Centraliza chamadas HTTP e converte falhas de conexão/HTTP em ErroApi.
    try:
        response = requests.get(url, params=parametros, headers=cabecalho, timeout=10)
        response.raise_for_status()

    except requests.exceptions.Timeout as erro:
        raise ErroApi(erro, 'Problema de tempo limite')

    except requests.exceptions.ConnectionError as erro:
        raise ErroApi(erro, 'Problema de conexão')

    except requests.exceptions.HTTPError as erro:
        raise ErroApi(erro, 'Problema de Http')


    return response

def _ler_json_resposta(response):
    try:
        return response.json()

    except requests.exceptions.JSONDecodeError as erro:
        raise ErroApi(erro, 'Resposta inválida da API') from erro

# irá realizar a busca de um filme
def buscar_filme(nome_filme):
    # Pesquisa títulos no TMDB e transforma a resposta resumida em objetos Filme.
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

    dados = _ler_json_resposta(response)

    lista_filmes = transformar_filmes(dados)

    return lista_filmes

def buscar_detalhes(filme):
    # Completa o filme selecionado com sinopse, duração, pôster e gêneros.
    parametros = {
        "language": "pt-BR",
    }

    response = fazer_requisicao(f'{BASE_URL}{MOVIE_DETAILS_ENDPOINT}{filme.id}', headers, parametros)

    dados = _ler_json_resposta(response)

    sinopse = (dados['overview'] or '').strip()
    if sinopse:
        filme.sinopse = sinopse
    else:
        filme.sinopse = None

    filme.duracao = dados['runtime']
    filme.poster = dados['poster_path']

    for genero in dados['genres']:
        id_e_genero = {'tmdb_id': genero['id'], 'nome': genero['name']}
        filme.generos.append(id_e_genero)

def buscar_disponibilidade(filme):
    # Carrega provedores disponíveis no Brasil e normaliza as ofertas.

    response = fazer_requisicao(f'{BASE_URL}{MOVIE_DETAILS_ENDPOINT}{filme.id}{MOVIE_PROVIDERS_ENDPOINT}',headers)

    dados = _ler_json_resposta(response)
    dados_brasil = dados['results'].get('BR')

    if dados_brasil is None:
        filme.disponibilidade = []
    else:
        filme.disponibilidade = organizar_disponibilidades(dados_brasil)
