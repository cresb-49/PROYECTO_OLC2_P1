from enum import Enum
import Abstracto.Exprecion as Exprecion

"""
Enum del tipo de operaciones artimeticas
"""
class OpcionOperacion(Enum):
    SUMA = 1
    RESTA = 2
    MUL = 3
    DIV = 4
    MOD = 5
    POT = 6


"""
Clase de la abstraccion de las operaciones aritmeticas

Raises:
    ValueError: El valor del hijo izquierdo de la operacion es None
    ValueError: El valor del hijo derecho de la operacion es None
"""
class Operacion(Exprecion):

    def __init__(self, linea, columna, izquierda: Exprecion, derecha: Exprecion, tipo: OpcionOperacion):
        super().__init__(linea, columna)
        self.TipoOperacion = ['+', '-', '*', '/', '%', '^']
        self.izquierda = izquierda
        self.derecha = derecha
        self.tipo = tipo

    def ejecutar(self, scope):
        result = None
        val_izquierdo = self.izquierda.ejecutar(scope)
        val_derecho = self.derecha.ejecutar(scope)
        if (val_derecho.value == None or val_izquierdo.value == None):
            if (val_izquierdo.value == None):
                raise ValueError("No se puede operar con un valor nulo Linea: " + self.linea + " ,Columna: " +
                                 self.columna + " ->  null " + self.TipoOperacion[self.tipo] + " " + val_derecho.value)
            else:
                raise ValueError("No se puede operar con un valor nulo Linea: " + self.linea + " ,Columna: " +
                                 self.columna + " ->  " + val_derecho.value + " " + self.TipoOperacion[self.tipo] + " null")

        # Debemos de verificar operacion entre tipos

        if (self.tipo == OpcionOperacion.SUMA):
            result = None
        elif (self.tipo == OpcionOperacion.RESTA):
            result = None
        elif (self.tipo == OpcionOperacion.MUL):
            result = None
        elif (self.tipo == OpcionOperacion.DIV):
            result = None
        elif (self.tipo == OpcionOperacion.MOD):
            result = None
        elif (self.tipo == OpcionOperacion.POT):
            result = None
        else:
            result = None
            
        return result

    def graficar(self, scope, graphviz, padre):
        num = graphviz.declaraciones.length + 1
        node = "nodo" + num + \
            ' [label="' + self.TipoOperacion[self.tipo] + '",shape="circle"];'
        graphviz.declaraciones.push(node)
        if (padre.length != 0):
            relacion = padre + ' -> ' + "nodo" + num
            graphviz.relaciones.push(relacion)

        self.izquierda.graficar(scope, graphviz, ("nodo" + num))
        self.derecha.graficar(scope, graphviz, ("nodo" + num))
