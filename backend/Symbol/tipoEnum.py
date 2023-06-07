from enum import Enum


class TipoEnum(Enum):
    NUMBER = "number"
    BOOLEAN = "boolean"
    STRING = "string"
    ANY = "any"
    NULL = "null"
    STRUCT = "interface"
    ERROR = "error"
