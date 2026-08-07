from config import BASE_URL, API_KEY, MOVIE_SEARCH_ENDPOINT
import requests
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



    response = requests.get(BASE_URL + MOVIE_SEARCH_ENDPOINT, params=parametros, headers=headers)
    print(response.json())
buscar_filme('Interestelar')


