from Abstract.abstract import Abstract


class Relacional(Abstract):
    def __init__(self, linea, columna, expresion_izquierda, expresion_derecha, tipo_operacion):
        super().__init__(linea, columna)
        self.expresion_izquierda = expresion_izquierda
        self.expresion_derecha = expresion_derecha
        self.tipo_operacion = tipo_operacion

    def ejecutar(self, scope):
        val_izquierdo = self.expresion_izquierda.ejecutar(scope)
        val_derecho = self.expresion_derecha.ejecutar(scope)

        if (self.tipo == "==="):
            return val_izquierdo == val_derecho
        elif (self.tipo == "!=="):
            return val_izquierdo != val_derecho
        elif (self.tipo == "<"):
            return val_izquierdo < val_derecho
        elif (self.tipo == ">"):
            return val_izquierdo > val_derecho
        elif (self.tipo == "<="):
            return val_izquierdo <= val_derecho
        elif (self.tipo == ">="):
            return val_izquierdo >= val_derecho
