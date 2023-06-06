from enum import Enum


class TipoEnum(Enum):
    NUMBER = 0
    BOOLEAN = 1
    STRING = 2
    ANY = 3
    STRUCT = 4
    ERROR = 5


class Tipo():
    """
    Tipo de datos con los primitivos en enum, y un tipo secudario usado en any y struct
    """

    def __init__(self, tipo: TipoEnum, tipo_secundario):
        self.type = tipo
        self.tipo_secundario = tipo_secundario

    def get_tipo(self):
        return self.type

    def get_tipo_string(self):
        if (self.type == TipoEnum.NUMBER):
            return 'number'
        elif (self.type == TipoEnum.BOOLEAN):
            return 'boolean'
        elif (self.type == TipoEnum.STRING):
            return 'string'
        elif (self.type == TipoEnum.ANY):
            return 'any'
        elif (self.type == TipoEnum.STRUCT):
            return 'struct'
        elif (self.type == TipoEnum.ERROR):
            return 'error'

    def get_tipo_secundario(self):
        return self.tipo_secundario
