from app.transformador import transformar_filmes

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
