from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum


class Logico(Abstract):
    def __init__(self, resultado, linea, columna, expresion_izquierda, expresion_derecha, tipo_operacion):
        super().__init__(resultado, linea, columna)
        self.expresion_izquierda = expresion_izquierda
        self.expresion_derecha = expresion_derecha
        self.tipo_operacion = tipo_operacion

    def verificarTipos(self, val_izq, val_derecho):
        # extraemos el tipo de la exprecion izquierda de la op
        tipo_exprecion_izquierda = val_izq["tipo"]
        tipo_exprecion_der = val_derecho["tipo"]
        if (tipo_exprecion_izquierda == tipo_exprecion_der and (tipo_exprecion_izquierda == TipoEnum.BOOLEAN)):
            # si se trata de una suma enviamos a validarla
            return True
        else:
            concat = 'Error: Tipos no coinciden para la operacion, Se esperaba BOOLEAN y BOOLEAN y se recibio ', tipo_exprecion_izquierda.value, ' y ', tipo_exprecion_der.value, ' linea:', self.linea, 'columna', self.columna
            self.resultado.add_error(
                'Semantico', concat, self.linea, self.columna)
            return False

    def ejecutar(self, scope):
        val_derecho = self.expresion_derecha.ejecutar(scope)
        val_izq = self.expresion_izquierda.ejecutar(scope)
        if (self.verificarTipos(val_izq, val_derecho)):
            if (self.tipo_operacion == "&&"):
                val_izquierdo = self.expresion_izquierda.ejecutar(scope)
                result = val_izquierdo['value'] and val_derecho['value']
                return {"value": result, "tipo": TipoEnum.BOOLEAN, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == "||"):
                val_izquierdo = self.expresion_izquierda.ejecutar(scope)
                result = val_izquierdo['value'] or val_derecho['value']
                return {"value": result, "tipo": TipoEnum.BOOLEAN, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == "!"):
                result = not val_derecho['value']
                return {"value": result, "tipo": TipoEnum.BOOLEAN, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        else:
            # print('Debuj-> Primitivo ->', self)
            return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        result = graphviz.add_nodo(self.tipo_operacion, padre)
        self.expresion_izquierda.graficar(graphviz, result)
        self.expresion_derecha.graficar(graphviz, result)
