#Converte a estrutura de uma fonte de dados para a estrutura do nosso domínio
from app.filme import Filme

def mapear_filme(linha):
    filme1 = Filme(linha[2], linha[3], linha[4], linha[1])
    filme1.sinopse = linha[5]
    filme1.duracao = linha[6]

    return filme1
