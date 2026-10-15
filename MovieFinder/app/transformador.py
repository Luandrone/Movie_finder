# Adapta respostas JSON do TMDB para as estruturas internas da aplicação.
from app.filme import Filme


def transformar_filmes(dados):
    # Converte resultados resumidos da busca em objetos Filme.
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
    # Padroniza um provedor no formato usado pelo domínio e pelo banco.
    dados_transformados = {
        'provider_id': provedor['provider_id'],
        'provider_name': provedor['provider_name'],
        'tipo': tipo,
        'logo_path': provedor['logo_path'],
        'link': link
    }

    return dados_transformados

def organizar_disponibilidades(dados_brasil):
    # Achata as listas regionais em registros individuais por tipo de oferta.
    lista_disponibilidades = []

    for tipo in ['buy', 'rent', 'flatrate']:
        provedores = dados_brasil.get(tipo, [])

        for provedor in provedores:
            disponibilidade = transformar_disponibilidade(provedor, tipo, dados_brasil.get('link'))
            lista_disponibilidades.append(disponibilidade)

    return lista_disponibilidades