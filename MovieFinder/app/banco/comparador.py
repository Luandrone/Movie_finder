def comparar_filmes(filme, filme_banco):
    alteracoes = []
    if filme.titulo != filme_banco.titulo:
        alteracoes.append(
            {
                'campo': 'titulo',
                'anterior': filme_banco.titulo,
                'novo': filme.titulo
            }
        )
    if filme.ano != filme_banco.ano:
        alteracoes.append({
            'campo': 'ano',
            'anterior': filme_banco.ano,
            'novo': filme.ano
        })

    if filme.nota != filme_banco.nota:
        alteracoes.append(
            {
                'campo': 'nota',
                'anterior': filme_banco.nota,
                'novo': filme.nota
            }

        )
    if filme.sinopse != filme_banco.sinopse:
        alteracoes.append(
            {
                'campo': 'sinopse',
                'anterior': filme_banco.sinopse,
                'novo': filme.sinopse
            }

        )
    if filme.duracao != filme_banco.duracao:
        alteracoes.append(
            {
                'campo': 'duracao',
                'anterior': filme_banco.duracao,
                'novo': filme.duracao
            }

        )

    return alteracoes


def comparar_disponibilidades(disponibilidades_api, disponibilidades_banco):
    novas = []
    excluidas = []
    atualizadas = []
    chaves_api = set()
    campos = ['provider_name', 'logo_path', 'link']

    disponibilidades_por_chave = {}

    for disponibilidade_banco in disponibilidades_banco:
        chave_banco = (
            disponibilidade_banco['provider_id'],
            disponibilidade_banco['tipo'],
        )
        disponibilidades_por_chave[chave_banco] = disponibilidade_banco

    for disponibilidade_api in disponibilidades_api:
        chave_api = (
            disponibilidade_api['provider_id'],
            disponibilidade_api['tipo']
        )
        chaves_api.add(chave_api)

        if chave_api not in disponibilidades_por_chave:
            novas.append(disponibilidade_api)

        else:
            disponibilidade_banco = disponibilidades_por_chave[chave_api]

            alteracoes_disponibilidade = []

            for campo in campos:
                if disponibilidade_api[campo] != disponibilidade_banco[campo]:
                    alteracoes_disponibilidade.append({
                        'campo': campo,
                        'anterior': disponibilidade_banco[campo],
                        'novo': disponibilidade_api[campo]
                    })

            if alteracoes_disponibilidade:
                atualizadas.append({
                    'provider_id': disponibilidade_api['provider_id'],
                    'tipo': disponibilidade_api['tipo'],
                    'alteracoes': alteracoes_disponibilidade
                })

    chaves_banco = set(disponibilidades_por_chave.keys())
    chaves_excluidas = chaves_banco - chaves_api

    for chave in chaves_excluidas:
        excluidas.append(disponibilidades_por_chave[chave])

    return {
        'novas': novas,
        'atualizadas': atualizadas,
        'excluidas': excluidas
}

def comparar_generos(generos_api, generos_banco):
    ids_generos_api = set()
    ids_generos_banco = set()

    for genero in generos_api:
        ids_generos_api.add(genero['tmdb_id'])

    for genero in generos_banco:
        ids_generos_banco.add(genero['tmdb_id'])

    ids_generos_novos = ids_generos_api - ids_generos_banco
    ids_generos_excluidos = ids_generos_banco - ids_generos_api

    generos_novos = []
    generos_excluidos = []

    for genero in generos_api:
        if genero['tmdb_id'] in ids_generos_novos:
            generos_novos.append(genero)

    for genero in generos_banco:
        if genero['tmdb_id'] in ids_generos_excluidos:
            generos_excluidos.append(genero)

    return {
        'novos': generos_novos,
        'excluidos': generos_excluidos
    }






