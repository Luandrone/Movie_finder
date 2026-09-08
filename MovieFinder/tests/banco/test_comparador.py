from app.banco.comparador import comparar_filmes, comparar_disponibilidades
from app.filme import Filme
from teste_postgres import resultado


def test_comparar_filmes_divergentes():
    filme_falso = Filme('The Batman', 2022, 8.0, 123, 'Nova sinopse', 176)
    filme_falso_banco = Filme('Batman', 2020, 7.0, 123, 'Sinopse antiga', 150)
    resultado = comparar_filmes(filme_falso, filme_falso_banco)

    assert resultado == [
        {
            'campo': 'titulo',
            'anterior': 'Batman',
            'novo': 'The Batman'
        },
        {
            'campo': 'ano',
            'anterior': 2020,
            'novo': 2022
        },
        {
            'campo': 'nota',
            'anterior': 7.0,
            'novo': 8.0
        },
        {
            'campo': 'sinopse',
            'anterior': 'Sinopse antiga',
            'novo': 'Nova sinopse'
        },
        {
            'campo': 'duracao',
            'anterior': 150,
            'novo': 176
        }
    ]


def test_comparar_filmes_iguais():
    filme_falso = Filme('Batman', 2020, 8.0, 123, 'sinopse', 176)
    filme_falso_banco = Filme('Batman', 2020, 8.0, 123, 'sinopse', 176)

    resultado = comparar_filmes(filme_falso, filme_falso_banco)

    assert resultado == []


def test_comparar_disponibilidades_sem_alteracoes():
    disponibilidades_banco_falso = [{
        'provider_id': 1899,
        'provider_name': 'HBO Max',
        'tipo': 'flatrate',
        'logo_path': '/hbo.jpg',
        'link': 'https://teste.com'
    }]

    disponibilidades_api_falso = [{
        'provider_id': 1899,
        'provider_name': 'HBO Max',
        'tipo': 'flatrate',
        'logo_path': '/hbo.jpg',
        'link': 'https://teste.com'
    }]

    resultado = comparar_disponibilidades(disponibilidades_api_falso, disponibilidades_banco_falso)

    assert resultado == {
        'novas': [],
        'atualizadas': [],
        'excluidas': []
    }


def test_comparar_disponibilidades_nova():
    disponibilidades_banco_falso = []
    disponibilidades_api_falso = [
        {
            'provider_id': 1899,
            'provider_name': 'HBO Max',
            'tipo': 'flatrate',
            'logo_path': '/hbo.jpg',
            'link': 'https://teste.com'
        }
    ]

    resultado = comparar_disponibilidades(disponibilidades_api_falso, disponibilidades_banco_falso)

    assert resultado == {
        'novas': [
            {
                'provider_id': 1899,
                'provider_name': 'HBO Max',
                'tipo': 'flatrate',
                'logo_path': '/hbo.jpg',
                'link': 'https://teste.com'
            }
        ],
        'atualizadas': [],
        'excluidas': []
    }


def test_comparar_disponibilidades_atualizada():
    disponibilidades_banco_falso = [
        {
            'provider_id': 1899,
            'provider_name': 'HBO Max',
            'tipo': 'flatrate',
            'logo_path': '/hbo-antigo.jpg',
            'link': 'https://teste-antigo.com'
        }
    ]

    disponibilidades_api_falso = [
        {
            'provider_id': 1899,
            'provider_name': 'Max',
            'tipo': 'flatrate',
            'logo_path': '/max.jpg',
            'link': 'https://teste-novo.com'
        }
    ]

    resultado = comparar_disponibilidades(disponibilidades_api_falso, disponibilidades_banco_falso)

    assert resultado == {
        'novas': [],
        'atualizadas': [
            {
                'campo': 'provider_name',
                'anterior': 'HBO Max',
                'novo': 'Max'
            },
            {
                'campo': 'logo_path',
                'anterior': '/hbo-antigo.jpg',
                'novo': '/max.jpg'
            },
            {
                'campo': 'link',
                'anterior': 'https://teste-antigo.com',
                'novo': 'https://teste-novo.com'
            }
        ],
        'excluidas': []
    }


def test_comparar_disponibilidades_excluida():
    disponibilidades_banco_falso = [
        {
            'provider_id': 10,
            'provider_name': 'Amazon Video',
            'tipo': 'rent',
            'logo_path': '/amazon.jpg',
            'link': 'https://teste.com'
        }
    ]

    disponibilidades_api_falso = []

    resultado = comparar_disponibilidades(disponibilidades_api_falso, disponibilidades_banco_falso)

    assert resultado == {
        'novas': [],
        'atualizadas': [],
        'excluidas': [
            {
                'provider_id': 10,
                'provider_name': 'Amazon Video',
                'tipo': 'rent',
                'logo_path': '/amazon.jpg',
                'link': 'https://teste.com'
            }
        ]
    }


def test_comparar_disponibilidades_mista():
    disponibilidades_banco_falso = [
        {
            'provider_id': 1899,
            'provider_name': 'HBO Max',
            'tipo': 'flatrate',
            'logo_path': '/hbo-antigo.jpg',
            'link': 'https://antigo.com'
        },
        {
            'provider_id': 2,
            'provider_name': 'Apple TV Store',
            'tipo': 'buy',
            'logo_path': '/apple.jpg',
            'link': 'https://apple.com'
        },
        {
            'provider_id': 10,
            'provider_name': 'Amazon Video',
            'tipo': 'rent',
            'logo_path': '/amazon.jpg',
            'link': 'https://amazon.com'
        }
    ]
    disponibilidades_api_falso = [
        {
            'provider_id': 50,
            'provider_name': 'Disney+',
            'tipo': 'flatrate',
            'logo_path': '/disney.jpg',
            'link': 'https://disney.com'
        },
        {
            'provider_id': 1899,
            'provider_name': 'Max',
            'tipo': 'flatrate',
            'logo_path': '/max.jpg',
            'link': 'https://novo.com'
        },
        {
            'provider_id': 2,
            'provider_name': 'Apple TV Store',
            'tipo': 'buy',
            'logo_path': '/apple.jpg',
            'link': 'https://apple.com'
        }
    ]

    resultado = comparar_disponibilidades(disponibilidades_api_falso, disponibilidades_banco_falso)

    assert resultado == {
        'novas': [
            {
                'provider_id': 50,
                'provider_name': 'Disney+',
                'tipo': 'flatrate',
                'logo_path': '/disney.jpg',
                'link': 'https://disney.com'
            }
        ],
        'atualizadas': [
            {
                'campo': 'provider_name',
                'anterior': 'HBO Max',
                'novo': 'Max'
            },
            {
                'campo': 'logo_path',
                'anterior': '/hbo-antigo.jpg',
                'novo': '/max.jpg'
            },
            {
                'campo': 'link',
                'anterior': 'https://antigo.com',
                'novo': 'https://novo.com'
            }
        ],
        'excluidas': [
            {
                'provider_id': 10,
                'provider_name': 'Amazon Video',
                'tipo': 'rent',
                'logo_path': '/amazon.jpg',
                'link': 'https://amazon.com'
            }]
    }
