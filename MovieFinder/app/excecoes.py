# Define a exceção usada para transportar falhas da integração com a API.
class ErroApi(Exception):
    def __init__(self, erro ,tipo):
        self.erro = erro
        self.tipo = tipo