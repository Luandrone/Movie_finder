from app.banco.comparador import comparar_filmes
from app.filme import Filme

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