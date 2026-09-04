from app.filme import Filme


def transformar_filmes(dados):
    lista_filmes = []
    for filme in dados['results']:
        data = (filme['release_date'] or '').strip()
        if data:
            ano = data[:4]
        else:
            ano = 'Desconhecido'
        objeto_filme = Filme(filme['title'], ano, filme['vote_average'], filme['id'])
        lista_filmes.append(objeto_filme)
    return lista_filmes


def transformar_disponibilidade(provedor, tipo, link):
    dados_transformados = {
        'provider_id': provedor['provider_id'],
        'provider_name': provedor['provider_name'],
        'tipo': tipo,
        'logo_path': provedor['logo_path'],
        'link': link
    }

    return dados_transformados