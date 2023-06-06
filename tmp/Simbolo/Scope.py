from Simbolo.Variables import Variables
from Simbolo.Funciones import Funciones
from Simbolo import Simbolo
from Instrucciones.Funcion import Funcion
from Abstracto.Tipo import Tipo


class Scope:
    def __init__(self, anterior) -> None:
        self.anterior = anterior
        self.variables = Variables()
        self.funciones = Funciones()

    def declarar_variable(self, identificador: str, valor: any, tipo: Tipo, linea, columna):
        try:
            self.variables.add(identificador, Simbolo(valor, identificador, tipo, linea, columna))
        except ValueError as error:
            print(f"Se produjo un error: {str(error)}")
    
    def modificar_variable(self,identificador:str,valor:any,tipo:Tipo):
        if self.variables.has(identificador) :
            self.variables.update(identificador,valor,tipo)
        else:
            raise ValueError ("No se modificar la variable porque no existe en el scope")

    def obtener_variable(self, identificador:str) -> Simbolo:
        scope = self
        while (scope != None):
            if (scope.variables.has(identificador)):
                return scope.variables.get(identificador)
            scope = scope.anterior
        return None

    def declarar_funcion(self, identificador:str, funcion: Funcion):
        try:
            self.funciones.add(identificador, funcion)
        except ValueError as error:
            print(f"Se produjo un error: {str(error)}")

    def obtener_funcion(self, identificador:str) -> Funcion:
        scope = self
        while (scope != None):
            if (scope.funciones.has(identificador)):
                return scope.funciones.get(identificador)
            scope = scope.anterior
        return None
