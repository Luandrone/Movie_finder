class Filme:
    def __init__(self, titulo='', ano=0, nota=0.0, id=0, sinopse='', duracao='', poster='', generos=None):
        if generos is None:
            generos = []
        self.titulo = titulo
        self.ano = ano
        self.nota = nota
        self.id = id
        self.sinopse = sinopse
        self.duracao = duracao
        self.poster = poster
        self.generos = generos


    def __str__(self):
        return f'Filme: {self.titulo} \nano: {self.ano} \nnota: {self.nota:.1f}\nid: {self.id}\nsinopse: {self.sinopse}\nduração: {self.duracao}\nposter: {self.poster}\ngeneros: {self.generos}'


