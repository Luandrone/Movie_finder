from decimal import Decimal

from app.banco.mapper import mapear_filme

def test_mapear_filme():
    linha_falsa = (
        1,
        123,
        'Batman',
        2021,
        Decimal('8.0'),
        'blabla',
        210
    )

    filme = mapear_filme(linha_falsa)

    assert filme.id == 123
    assert filme.titulo == 'Batman'
    assert filme.ano == 2021
    assert filme.nota == Decimal('8.0')
    assert filme.sinopse == 'blabla'
    assert filme.duracao == 210
