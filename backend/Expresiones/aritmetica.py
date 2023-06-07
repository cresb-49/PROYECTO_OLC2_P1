from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum

class Aritmetica(Abstract):
    def __init__(self, linea, columna, expresion_izquierda, expresion_derecha, tipo_operacion):
        super().__init__(linea, columna)
        self.expresion_izquierda = expresion_izquierda
        self.expresion_derecha = expresion_derecha
        self.tipo_operacion = tipo_operacion

    def verificarTipos(self):
        pass

    def ejecutar(self, scope):
        val_izquierdo = self.expresion_izquierda.ejecutar(scope)
        val_derecho = self.expresion_derecha.ejecutar(scope)

        # print('Debuj-> Aritmetica -> tipo_operacion: ',self.tipo_operacion)
        # print('Debuj-> Aritmetica -> Izquierdo: ',val_izquierdo)
        # print('Debuj-> Aritmetica -> Derecho: ',val_derecho)

        if (self.tipo_operacion == "+"):
            result = val_izquierdo['value'] + val_derecho['value']
            return {"value": result, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        elif (self.tipo_operacion == "-"):
            result = val_izquierdo['value'] - val_derecho['value']
            return {"value": result, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        elif (self.tipo_operacion == "*"):
            result = val_izquierdo['value'] * val_derecho['value']
            return {"value": result, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        elif (self.tipo_operacion == "/"):
            if val_derecho == 0:
                raise ValueError('Error: Divicion entre 0',
                                 'linea:', self.linea, 'columna', self.columna)
            result = val_izquierdo['value'] / val_derecho['value']
            return {"value": result, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        elif (self.tipo_operacion == "%"):
            result = val_izquierdo['value'] % val_derecho['value']
            return {"value": result, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        elif (self.tipo_operacion == "^"):
            result = val_izquierdo['value'] ** val_derecho['value']
            return {"value": result, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, scope, graphviz, subNameNode, padre):
        num = graphviz.declaraciones.length + 1
        node = "nodo" + num + ' [label="' + \
            self.tipo_operacion + '",shape="circle"];'
        graphviz.declaraciones.push(node)
        if (padre.length != 0):
            relacion = padre + ' -> ' + "nodo" + num
            graphviz.relaciones.push(relacion)

        self.izquierda.graficar(scope, graphviz, ("nodo" + num))
        self.derecha.graficar(scope, graphviz, ("nodo" + num))
