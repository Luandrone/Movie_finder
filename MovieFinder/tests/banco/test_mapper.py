from decimal import Decimal

from app.banco.mapper import mapear_filme, mapear_disponibilidade


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
    assert filme.ano == '2021'
    assert filme.nota == 8.0
    assert filme.sinopse == 'blabla'
    assert filme.duracao == 210

def test_mapear_disponibilidade():
    linha_falsa = (
        1,
        414906,
        2,
        'Apple TV Store',
        'buy',
        '/alguma-imagem',
        'https://algum-link.com'
                   )
    resultado = mapear_disponibilidade(linha_falsa)

    assert resultado == {
    'provider_id': 2,
    'provider_name': 'Apple TV Store',
    'tipo': 'buy',
    'logo_path': '/alguma-imagem',
    'link': 'https://algum-link.com'
}