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