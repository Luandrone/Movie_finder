class ErroApi(Exception):
    def __init__(self, erro ,tipo):
        self.erro = erro
        self.tipo = tipo