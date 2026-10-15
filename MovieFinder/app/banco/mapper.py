# Converte linhas do banco para os objetos e estruturas usados pelo domínio.
#Converte a estrutura do banco de dados para a estrutura do nosso domínio
from app.filme import Filme

def mapear_filme(linha):
    # Converte uma linha de tblFilmes em Filme e preserva a chave interna.
    filme = Filme(linha[2], str(linha[3]), float(linha[4]), linha[1])
    filme.id_banco = linha[0]
    filme.sinopse = linha[5]
    filme.duracao = linha[6]

    return filme

def mapear_disponibilidade(linha):
    # Converte uma linha de provedor para o formato compartilhado pela aplicação.
    disponibilidade = {}

    disponibilidade['provider_id'] = linha[2]
    disponibilidade['provider_name'] = linha[3]
    disponibilidade['tipo'] = linha[4]
    disponibilidade['logo_path'] = linha[5]
    disponibilidade['link'] = linha[6]

    return disponibilidade

def mapear_genero(linha):
    # Converte uma linha de gênero para o dicionário usado no domínio.
    genero = {'tmdb_id': linha[0], 'nome': linha[1]}

    return genero