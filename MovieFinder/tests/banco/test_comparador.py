from app.banco.comparador import comparar_filmes
from app.filme import Filme

def test_comparar_filmes_nota_diferente():
    filme_falso = Filme('Batman', 2020, 8.0, 123)
    filme_falso_banco = Filme('Batman', 2020, 7.0, 123)
    resultado = comparar_filmes(filme_falso, filme_falso_banco)

    assert resultado == [
        {
            'campo': 'nota',
            'anterior': 7.0,
            'novo': 8.0
        }
    ]