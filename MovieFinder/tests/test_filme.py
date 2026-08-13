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