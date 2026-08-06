class Filme:
    def __init__(self, titulo='', ano=0, nota=0.0, sinopse='', genero='', duracao=0.0):
        self.titulo = titulo
        self.ano = ano
        self.nota = nota
        self.sinopse = sinopse
        self.genero = genero
        self.duracao = duracao

    def mostrar_detalhes(self):
        return f'{self.titulo} \n{self.ano} \n{self.nota}'

filme1 = Filme(
    titulo = 'Interestelar',
    ano = 2014,
    nota = 8.7,
)
filme2 = Filme(
    titulo = 'Gladiador',
    ano = 2000,
    nota = 8.5,
)
filme3 = Filme(
    titulo = 'Cruzada',
    ano = 2005,
    nota = 7.3,
)
print(filme1.mostrar_detalhes())
print(filme2.mostrar_detalhes())
print(filme3.mostrar_detalhes())
