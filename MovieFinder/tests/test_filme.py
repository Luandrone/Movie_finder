from unittest.mock import Mock, patch

from app.api import buscar_filme
from app.config import BASE_URL, MOVIE_SEARCH_ENDPOINT, headers
from app.filme import Filme

def test_criar_filme():

    filme1 = Filme('Batman',2015, 7.5, 123)
    assert filme1.titulo == 'Batman'
    assert filme1.ano == 2015
    assert filme1.nota == 7.5
    assert filme1.id == 123

def test_valores_padrao_filme():

    filme2 = Filme()
    assert filme2.generos == []
    assert filme2.disponibilidade == {}

@patch('app.api.fazer_requisicao')
def test_buscar_filme(mock_requisicao):
    response_falso = {
        'results': [
            {
                'title': 'batman',
                'release_date': '2021-07-09',
                'vote_average': 7.5,
                'id': 123
            }
        ]
    }

    parametros = {
        'query': 'batman',
        'language': 'pt-BR',
        'region': 'BR',
        'page': 1,
        'include_adult': False

    }

    mock_response = Mock()
    mock_response.json.return_value = response_falso
    mock_requisicao.return_value = mock_response

    resultado = buscar_filme('batman')
    primeiro_filme = resultado[0]

    assert primeiro_filme.titulo == 'batman'
    assert primeiro_filme.ano == '2021'
    assert primeiro_filme.nota == 7.5
    assert primeiro_filme.id == 123
    mock_requisicao.assert_called_once_with(f'{BASE_URL}{MOVIE_SEARCH_ENDPOINT}', headers, parametros)

@patch('app.api.fazer_requisicao')
def test_buscar_filme_sem_data(mock_requisicao):
    response_falso = {
        'results': [
            {
                'title': 'batman',
                'release_date': '',
                'vote_average': 7.5,
                'id': 123
            }
        ]
    }

    mock_response = Mock()
    mock_response.json.return_value = response_falso
    mock_requisicao.return_value = mock_response

    resultado = buscar_filme('batman')
    primeiro_filme = resultado[0]

    assert primeiro_filme.ano == 'Desconhecido'

@patch('app.api.fazer_requisicao')
def test_buscar_filme_sem_release_date(mock_requisicao):
    response_falso = {
        'results': [
            {
                'title': 'batman',
                'release_date': None,
                'vote_average': 7.5,
                'id': 123
            }
        ]
    }

    mock_response = Mock()
    mock_response.json.return_value = response_falso
    mock_requisicao.return_value = mock_response

    resultado = buscar_filme('batman')
    primeiro_filme = resultado[0]

    assert primeiro_filme.ano == 'Desconhecido'