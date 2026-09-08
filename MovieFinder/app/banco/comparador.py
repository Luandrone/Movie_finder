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
    chaves_banco = []
    chaves_api = []

    for disponibilidade_banco in disponibilidades_banco:
        chaves_banco.append((disponibilidade_banco['provider_id'], disponibilidade_banco['tipo']))

    for disponibilidade_api in disponibilidades_api:
        chave_api = (disponibilidade_api['provider_id'], disponibilidade_api['tipo'])

        if chave_api not in chaves_banco:
            novas.append(disponibilidade_api)

        if chave_api in chaves_banco:
            for disponibilidade_banco in disponibilidades_banco:
                if disponibilidade_banco['provider_id'] == chave_api[0] and disponibilidade_banco['tipo'] == chave_api[
                    1]:

                    if disponibilidade_api['provider_name'] != disponibilidade_banco['provider_name']:
                        atualizadas.append({
                            'campo': 'provider_name',
                            'anterior': disponibilidade_banco['provider_name'],
                            'novo': disponibilidade_api['provider_name']
                        })

                    if disponibilidade_api['logo_path'] != disponibilidade_banco['logo_path']:
                        atualizadas.append({
                            'campo': 'logo_path',
                            'anterior': disponibilidade_banco['logo_path'],
                            'novo': disponibilidade_api['logo_path']
                        })

                    if disponibilidade_api['link'] != disponibilidade_banco['link']:
                        atualizadas.append({
                            'campo': 'link',
                            'anterior': disponibilidade_banco['link'],
                            'novo': disponibilidade_api['link']
                        })

    for disponibilidade_api in disponibilidades_api:
        chaves_api.append(
            (disponibilidade_api['provider_id'], disponibilidade_api['tipo'])
        )

    for disponibilidade_banco in disponibilidades_banco:
        chave_banco = (disponibilidade_banco['provider_id'], disponibilidade_banco['tipo'])

        if chave_banco not in chaves_api:
            excluidas.append(disponibilidade_banco)

    return {
        'novas': novas,
        'atualizadas': atualizadas,
        'excluidas': excluidas
    }
