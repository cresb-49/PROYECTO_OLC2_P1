import Tipo as Tipo


class Retorno():

    def __init__(self, value: any, tipo: Tipo):
        self.tipo_string = ['number', 'boolean','string', 'any', 'struct', 'error']
        self.value = value
        self.tipo = tipo
