#Converte a estrutura de uma fonte de dados para a estrutura do nosso domínio
from app.filme import Filme

def mapear_filme(linha):
    filme = Filme(linha[2], linha[3], linha[4], linha[1])
    filme.sinopse = linha[5]
    filme.duracao = linha[6]

    return filme
