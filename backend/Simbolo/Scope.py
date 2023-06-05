import Variables as Variables
import Funciones as Funciones
import Simbolo as Simbolo
import Instrucciones.Funcion as Funcion


class Scope:
    def __init__(self, anterior) -> None:
        self.anterior = anterior
        self.variables = Variables()
        self.funciones = Funciones()

    def declarar_variable(self, identificador, valor, tipo, linea, columna):
        try:
            self.variables.add(identificador, Simbolo(
                valor, identificador, tipo, linea, columna))
        except ValueError as error:
            print(f"Se produjo un error: {str(error)}")

    def obtener_variable(self, identificador) -> Simbolo:
        scope = self
        while (scope != None):
            if (scope.variables.has(identificador)):
                return scope.variables.get(identificador)
            scope = scope.anterior
        return None

    def declarar_funcion(self, identificador, funcion: Funcion):
        try:
            self.funciones.add(identificador, funcion)
        except ValueError as error:
            print(f"Se produjo un error: {str(error)}")

    def obtener_funcion(self, identificador) -> Simbolo:
        scope = self
        while (scope != None):
            if (scope.funciones.has(identificador)):
                return scope.funciones.get(identificador)
            scope = scope.anterior
        return None
