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
