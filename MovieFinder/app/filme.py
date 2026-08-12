class Filme:
    def __init__(self, titulo='', ano=0, nota=0.0, id=0, sinopse='', duracao='', poster='', generos=None, disponibilidade=None):
        if generos is None:
            generos = []
        if disponibilidade is None:
            disponibilidade = {}
        self.titulo = titulo
        self.ano = ano
        self.nota = nota
        self.id = id
        self.sinopse = sinopse
        self.duracao = duracao
        self.poster = poster
        self.generos = generos
        self.disponibilidade = disponibilidade


    def __str__(self):
        return (f'Filme: '
                f'{self.titulo} \nano: '
                f'{self.ano} \nnota: '
                f'{self.nota:.1f}\nid: '
                f'{self.id}\nsinopse: '
                f'{self.sinopse}\nduração: '
                f'{self.duracao}\nposter: '
                f'{self.poster}\ngeneros: '
                f'{self.generos}\n'
                f'disponibilidade: {self.disponibilidade}')


