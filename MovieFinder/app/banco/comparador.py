def comparar_filmes(filme, filme_banco):
    alteracao = []
    if filme.nota != filme_banco.nota:
        alteracao += [
            {
                'campo': 'nota',
                'anterior': filme_banco.nota,
                'novo': filme.nota
            }
        ]

    return alteracao