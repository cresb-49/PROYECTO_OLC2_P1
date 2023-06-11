from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum


class Relacional(Abstract):
    def __init__(self, resultado, linea, columna, expresion_izquierda, expresion_derecha, tipo_operacion):
        super().__init__(resultado, linea, columna)
        self.expresion_izquierda = expresion_izquierda
        self.expresion_derecha = expresion_derecha
        self.tipo_operacion = tipo_operacion

    def verificarTipos(self, val_izq, val_derecho):
        # extraemos el tipo de la exprecion izquierda de la op
        if(val_izq == None or val_derecho == None):
            return False
        tipo_exprecion_izquierda = val_izq["tipo"]
        tipo_exprecion_der = val_derecho["tipo"]
        if (tipo_exprecion_izquierda == tipo_exprecion_der and (tipo_exprecion_izquierda == TipoEnum.NUMBER or tipo_exprecion_izquierda == TipoEnum.STRING)):
            # si se trata de una suma enviamos a validarla
            return True
        else:
            concat = f'Tipos no coinciden para la operacion, Se esperaba number {self.tipo_operacion} number o string {self.tipo_operacion} string y se recibio {tipo_exprecion_izquierda.value} {self.tipo_operacion} {tipo_exprecion_der.value}'
            self.resultado.add_error(
                'Semantico', concat, self.linea, self.columna)
            print(concat)
            return False

    def ejecutar(self, scope):
        val_izquierdo = self.expresion_izquierda.ejecutar(scope)
        val_derecho = self.expresion_derecha.ejecutar(scope)

        if (self.verificarTipos(val_izquierdo, val_derecho)):
            if (self.tipo_operacion == "==="):
                result = val_izquierdo['value'] == val_derecho['value']
                return {"value": result, "tipo": TipoEnum.BOOLEAN, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == "!=="):
                result = val_izquierdo['value'] != val_derecho['value']
                return {"value": result, "tipo": TipoEnum.BOOLEAN, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == "<"):
                result = val_izquierdo['value'] < val_derecho['value']
                return {"value": result, "tipo": TipoEnum.BOOLEAN, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == ">"):
                result = val_izquierdo['value'] > val_derecho['value']
                return {"value": result, "tipo": TipoEnum.BOOLEAN, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == "<="):
                result = val_izquierdo['value'] <= val_derecho['value']
                return {"value": result, "tipo": TipoEnum.BOOLEAN, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == ">="):
                result = val_izquierdo['value'] >= val_derecho['value']
                return {"value": result, "tipo": TipoEnum.BOOLEAN, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        else:
            # print('Debuj-> Primitivo ->', self)
            return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        result = graphviz.add_nodo(self.tipo_operacion, padre)
        self.expresion_izquierda.graficar(graphviz, result)
        self.expresion_derecha.graficar(graphviz, result)
