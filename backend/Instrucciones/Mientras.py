from Abstracto.Instruccion import Instruccion
from Abstracto.Exprecion import Exprecion
from Abstracto.Tipo import Tipo
from Abstracto.Tipo import TipoEnum
from Simbolo.Scope import Scope
from Sentencias import Sentencias

from Instrucciones.Detener import Detener
from Instrucciones.Continuar import Continuar
from Instrucciones.Retornar import Retornar


class Mientras(Instruccion):
    def __init__(self, linea, columna, condicion: Exprecion, sentencias: Sentencias | None):
        super().__init__(linea, columna)
        self.condicion = condicion
        self.sentencias = sentencias

    def ejecutar(self, scope: Scope) -> any:
        condicion = self.condicion.ejecutar(scope)

        # Debemos de verificar el boolean de un any
        if (condicion.tipo.get_tipo() != TipoEnum.BOOLEAN):
            raise ValueError(
                "La condicion de Mientras no es de tipo Boolean Linea: "+self.linea+" ,Columna: "+self.columna)

        while (condicion.value):
            result = self.sentencias.ejecutar(scope)
            if (isinstance(result, Detener)):
                break
            elif (isinstance(result, Continuar)):
                continue
            elif (isinstance(result, Retornar)):
                return result

            condicion = self.condicion.ejecutar(scope)
            # Debemos de verificar el boolean de un any
            if (condicion.tipo.get_tipo() != TipoEnum.BOOLEAN):
                raise ValueError(
                    "La condicion de Mientras no es de tipo Boolean Linea: "+self.linea+" ,Columna: "+self.columna)
