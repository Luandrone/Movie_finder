class Filme:
    def __init__(self, titulo='', ano=0, nota=0.0, sinopse='', genero='', duracao=0.0):
        self.titulo = titulo
        self.ano = ano
        self.nota = nota
        self.sinopse = sinopse
        self.genero = genero
        self.duracao = duracao

    def __str__(self):
        return f'Filme: {self.titulo} \nano: {self.ano} \nnota: {self.nota:.1f}'


