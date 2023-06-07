from Abstract.abstract import Abstract

class Aritmetica(Abstract):
    def __init__(self, linea, columna, expresion_izquierda, expresion_derecha, tipo_operacion):
        super().__init__(linea, columna)
        self.expresion_izquierda = expresion_izquierda
        self.expresion_derecha = expresion_derecha
        self.tipo_operacion = tipo_operacion

    def ejecutar(self, scope):
        val_izquierdo = self.expresion_izquierda.ejecutar(scope)
        val_derecho = self.expresion_derecha.ejecutar(scope)
        
        #print('Debuj-> Aritmetica -> tipo_operacion: ',self.tipo_operacion)
        #print('Debuj-> Aritmetica -> Izquierdo: ',val_izquierdo)
        #print('Debuj-> Aritmetica -> Derecho: ',val_derecho)
        
        if (self.tipo_operacion == "+"):
            result = val_izquierdo['value'] + val_derecho['value']
            return {"value": result, "tipo": "number", "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        elif (self.tipo_operacion == "-"):
            result = val_izquierdo['value'] - val_derecho['value']
            return {"value": result, "tipo": "number", "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        elif (self.tipo_operacion == "*"):
            result = val_izquierdo['value'] * val_derecho['value']
            return {"value": result, "tipo": "number", "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        elif (self.tipo_operacion == "/"):
            if val_derecho == 0:
                raise ValueError ('Error: Divicion entre 0','linea:',self.linea,'columna',self.columna)
            result = val_izquierdo['value'] / val_derecho['value']
            return {"value": result, "tipo": "number", "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        elif (self.tipo_operacion == "%"):
            result = val_izquierdo['value'] % val_derecho['value']
            return {"value": result, "tipo": "number", "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        elif (self.tipo_operacion == "^"):
            result = val_izquierdo['value'] ** val_derecho['value']
            return {"value": result, "tipo": "number", "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        