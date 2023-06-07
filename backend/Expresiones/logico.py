from Abstract.abstract import Abstract


class Logico(Abstract):
    def __init__(self, linea, columna, expresion_izquierda, expresion_derecha, tipo_operacion):
        super().__init__(linea, columna)
        self.expresion_izquierda = expresion_izquierda
        self.expresion_derecha = expresion_derecha
        self.tipo_operacion = tipo_operacion

    def ejecutar(self, scope):
        val_derecho = self.expresion_derecha.ejecutar(scope)

        if (self.tipo_operacion == "&&"):
            val_izquierdo = self.expresion_izquierda.ejecutar(scope)
            result = val_izquierdo['value'] and val_derecho['value']
            return {"value": result, "tipo": "boolean", "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        elif (self.tipo_operacion == "||"):
            val_izquierdo = self.expresion_izquierda.ejecutar(scope)
            result = val_izquierdo['value'] or val_derecho['value']
            return {"value": result, "tipo": "boolean", "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        elif (self.tipo_operacion == "!"):
            result = not val_derecho['value']
            return {"value": result, "tipo": "boolean", "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, scope, graphviz, subNameNode, padre):
        num = graphviz.declaraciones.length + 1
        node = "nodo" + num + \
            '[label="' + self.tipo_operacion + '",shape="circle"];'
        graphviz.declaraciones.push(node)
        if (padre.length != 0):
            relacion = padre + ' -> ' + "nodo" + num
            graphviz.relaciones.push(relacion)
            
        self.izquierda.graficar(scope, graphviz, ("nodo" + num))
        self.derecha.graficar(scope, graphviz, ("nodo" + num))
