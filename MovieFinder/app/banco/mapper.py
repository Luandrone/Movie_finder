#Converte a estrutura do banco de dados para a estrutura do nosso domínio
from app.filme import Filme

def mapear_filme(linha):
    filme = Filme(linha[2], str(linha[3]), float(linha[4]), linha[1])
    filme.sinopse = linha[5]
    filme.duracao = linha[6]

    return filme

def mapear_disponibilidade(linha):
    disponibilidade = {}

    disponibilidade['provider_id'] = linha[2]
    disponibilidade['provider_name'] = linha[3]
    disponibilidade['tipo'] = linha[4]
    disponibilidade['logo_path'] = linha[5]
    disponibilidade['link'] = linha[6]

    return disponibilidade