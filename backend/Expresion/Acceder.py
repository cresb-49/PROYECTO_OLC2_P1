import Abstracto.Exprecion as Exprecion
import Abstracto.Retorno as Retorno
from Simbolo.Scope import Scope

class Acceder(Exprecion):
    def __init__(self, linea, columna, identificador):
        super().__init__(linea, columna)
        self.identificador = identificador

    def ejecutar(self, scope: Scope) -> Retorno:
        recuperacion = scope.obtenerVariable(self.identificador);
        if (recuperacion == None):
            raise ValueError("La variable \"" + self.identificador + "\" no existe, Linea: " + self.linea + " ,Columna: " + self.columna);
        
        #TODO:establecer el tipo de retorno logica no hecha
        return Retorno(recuperacion.valor,None)

    def graficar(self, scope, graphviz, padre):
        num = graphviz.declaraciones.length + 1
        node = "nodo" + num + ' [label="<f0> ID |<f1> ' + self.identificador + '"];'
        graphviz.declaraciones.push(node)
        if (padre.length != 0):
            relacion = padre + ' -> ' + "nodo" + num
            graphviz.relaciones.push(relacion)
        
