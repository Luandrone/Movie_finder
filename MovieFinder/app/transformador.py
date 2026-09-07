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

def organizar_disponibilidades(dados_brasil):
    lista_disponibilidades = []

    for tipo in ['buy', 'rent', 'flatrate']:
        provedores = dados_brasil.get(tipo, [])

        for provedor in provedores:
            disponibilidade = transformar_disponibilidade(provedor, tipo, dados_brasil.get('link'))
            lista_disponibilidades.append(disponibilidade)

    return lista_disponibilidades