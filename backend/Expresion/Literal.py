import Abstracto.Exprecion as Exprecion
import Abstracto.Retorno as Retorno
import Abstracto.Tipo as Tipo

class Literal(Exprecion):
    def __init__(self, linea, columna, valor, tipo):
        super().__init__(linea, columna)
        self.valor = valor
        self.tipo = tipo

    def ejecutar(self, scope):
        if (self.tipo == Tipo.NUMBER):
            return Retorno(self.valor,Tipo.NUMBER)
        elif (self.tipo == Tipo.BOOLEAN):
            return Retorno(self.valor,Tipo.BOOLEAN)
        elif (self.tipo == Tipo.STRING):
            return Retorno(self.valor,Tipo.STRING)
        elif (self.tipo == Tipo.ANY):
            return Retorno(self.valor,Tipo.ANY)
        elif (self.tipo == Tipo.STRUCT):
            return Retorno(self.valor,Tipo.STRUCT)
        elif (self.tipo == Tipo.ERROR):
            return Retorno(self.valor,Tipo.ERROR)

    def graficar(self, scope, graphviz, padre):
        num = graphviz.declaraciones.length + 1;
        node = "nodo" + num + ' [label="<f0> '+Retorno.tipo_string[self.tipo]+' |<f1> ' + self.valor + '"];'
        graphviz.declaraciones.push(node);
        if (padre.length != 0):
            relacion = padre + ' -> ' + "nodo" + num
            graphviz.relaciones.push(relacion);
        
        
