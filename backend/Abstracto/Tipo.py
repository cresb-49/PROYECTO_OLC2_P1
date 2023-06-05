from enum import Enum

class Tipo(Enum):
    NUMBER = 0,
    BOOLEAN = 1,
    STRING = 2,
    ANY = 3,
    STRUCT = 4,
    ERROR = 5,
