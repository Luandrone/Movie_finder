from app.api import buscar_filme
from app.config import MOVIE_SEARCH_ENDPOINT, BASE_URL, headers
from app.filme import Filme
from app.transformador import transformar_filmes, transformar_disponibilidade, organizar_disponibilidades
from unittest.mock import Mock, patch


def test_transformar_filmes():
    dados_falsos = {
        'results': [
            {
                'title': 'Batman',
                'release_date': '2021-07-09',
                'vote_average': 7.5,
                'id': 123
            }
        ]
    }

    resultado = transformar_filmes(dados_falsos)

    assert resultado[0].titulo == 'Batman'
    assert resultado[0].ano == '2021'
    assert resultado[0].nota == 7.5
    assert resultado[0].id == 123


def test_transformar_filmes_sem_data():
    dados_falsos = {
        'results': [
            {
                'title': 'batman',
                'release_date': '',
                'vote_average': 7.5,
                'id': 123
            }
        ]
    }

    resultado = transformar_filmes(dados_falsos)
    primeiro_filme = resultado[0]

    assert primeiro_filme.ano == 'Desconhecido'


def test_transformar_filmes_sem_release_date():
    dados_falsos = {
        'results': [
            {
                'title': 'batman',
                'release_date': None,
                'vote_average': 7.5,
                'id': 123
            }
        ]
    }

    resultado = transformar_filmes(dados_falsos)
    primeiro_filme = resultado[0]

    assert primeiro_filme.ano == 'Desconhecido'


@patch('app.api.fazer_requisicao')
@patch('app.api.transformar_filmes')
def test_buscar_filme(mock_transformar, mock_requisicao):
    dados_falsos = {
        'results': [
            {
                'title': 'batman',
                'release_date': None,
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
    filme_falso = Filme('Batman', 'Desconhecido', 7.5, 123)
    lista_de_filmes_falsa = [filme_falso]

    mock_response.json.return_value = dados_falsos
    mock_requisicao.return_value = mock_response
    mock_transformar.return_value = lista_de_filmes_falsa

    resultado = buscar_filme('batman')

    mock_transformar.assert_called_once_with(dados_falsos)
    assert resultado is lista_de_filmes_falsa
    mock_requisicao.assert_called_once_with(f'{BASE_URL}{MOVIE_SEARCH_ENDPOINT}', headers, parametros)


def test_transformar_disponibilidade():
    provedor_falso = {
        'provider_id': 1899,
        'provider_name': 'HBO Max',
        'logo_path': '/logo.jpg',
        'display_priority': 8
    }

    tipo = 'flatrate'
    link = 'https://www.themoviedb.org/movie/123/watch?locale=BR'

    resultado = transformar_disponibilidade(provedor_falso, tipo, link)

    assert resultado == {
        'link': 'https://www.themoviedb.org/movie/123/watch?locale=BR',
        'logo_path': '/logo.jpg',
        'provider_id': 1899,
        'provider_name': 'HBO Max',
        'tipo': 'flatrate'
    }

def test_organizar_disponibilidades():
    dados_brasil_falso = {
    'link': 'https://teste.com',
    'buy': [
        {
            'provider_id': 2,
            'provider_name': 'Apple TV Store',
            'logo_path': '/apple.jpg'
        }
    ],
    'rent': [
        {
            'provider_id': 10,
            'provider_name': 'Amazon Video',
            'logo_path': '/amazon.jpg'
        }
    ],
    'flatrate': [
        {
            'provider_id': 1899,
            'provider_name': 'HBO Max',
            'logo_path': '/hbo.jpg'
        }
    ]
}

    resultado = organizar_disponibilidades(dados_brasil_falso)

    assert resultado == [
    {
        'provider_id': 2,
        'provider_name': 'Apple TV Store',
        'tipo': 'buy',
        'logo_path': '/apple.jpg',
        'link': 'https://teste.com'
    },
    {
        'provider_id': 10,
        'provider_name': 'Amazon Video',
        'tipo': 'rent',
        'logo_path': '/amazon.jpg',
        'link': 'https://teste.com'
    },
    {
        'provider_id': 1899,
        'provider_name': 'HBO Max',
        'tipo': 'flatrate',
        'logo_path': '/hbo.jpg',
        'link': 'https://teste.com'
    }
]

def test_organizar_disponibilidades_sem_provedor():
    dados_brasil_falso = {
        'link': 'https://teste.com',
        'buy': [
            {
                'provider_id': 2,
                'provider_name': 'Apple TV Store',
                'logo_path': '/apple.jpg'
            }
        ],
        'rent': [
            {
                'provider_id': 10,
                'provider_name': 'Amazon Video',
                'logo_path': '/amazon.jpg'
            }
        ]
    }

    resultado = organizar_disponibilidades(dados_brasil_falso)

    assert resultado == [
    {
        'provider_id': 2,
        'provider_name': 'Apple TV Store',
        'tipo': 'buy',
        'logo_path': '/apple.jpg',
        'link': 'https://teste.com'
    },
    {
        'provider_id': 10,
        'provider_name': 'Amazon Video',
        'tipo': 'rent',
        'logo_path': '/amazon.jpg',
        'link': 'https://teste.com'
    }
]
