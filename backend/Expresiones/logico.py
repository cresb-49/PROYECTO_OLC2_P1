from Abstract.return__  import Return
from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum
from Symbol.generador import Generador


class Logico(Abstract):
    def __init__(self, resultado, linea, columna, expresion_izquierda, expresion_derecha, tipo_operacion):
        super().__init__(resultado, linea, columna)
        self.expresion_izquierda = expresion_izquierda
        self.expresion_derecha = expresion_derecha
        self.tipo_operacion = tipo_operacion

    def __str__(self):
        return f"Resultado: {self.resultado}\nLínea: {self.linea}\nColumna: {self.columna}\nExpresión Izquierda: {self.expresion_izquierda}\nExpresión Derecha: {self.expresion_derecha}\nTipo de Operación: {self.tipo_operacion}"

    def verificarTipos(self, val_izq, val_derecho):
        if (val_izq == None or val_derecho == None):
            return False
        # extraemos el tipo de la exprecion izquierda de la op
        tipo_exprecion_der = val_derecho["tipo"]
        if self.tipo_operacion == "!":
            if tipo_exprecion_der == TipoEnum.BOOLEAN:
                return True
            else:
                concat = f'Se esperaba boolean para la operacion "{self.tipo_operacion}" boolean y se recibio: {self.tipo_operacion} {tipo_exprecion_der.value}'
                self.resultado.add_error(
                    'Semantico', concat, self.linea, self.columna)
                return False
        else:
            tipo_exprecion_izquierda = val_izq["tipo"]
            if (tipo_exprecion_izquierda == tipo_exprecion_der and (tipo_exprecion_izquierda == TipoEnum.BOOLEAN)):
                # si se trata de una suma enviamos a validarla
                return True
            else:
                concat = f'Tipos no coinciden para la operacion, Se esperaba boolean {self.tipo_operacion} boolean y se recibio {tipo_exprecion_izquierda.value} {self.tipo_operacion} {tipo_exprecion_der.value}'
                self.resultado.add_error(
                    'Semantico', concat, self.linea, self.columna)
                return False

    def ejecutar(self, scope):
        # print(self)
        val_derecho = self.expresion_derecha.ejecutar(scope)
        if self.expresion_izquierda != None:
            val_izq = self.expresion_izquierda.ejecutar(scope)
        else:
            val_izq = None
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
        if self.tipo_operacion != "!":
            self.expresion_izquierda.graficar(graphviz, result)
        self.expresion_derecha.graficar(graphviz, result)

    def generar_c3d(self, scope):
            gen_aux = Generador()
            generador = gen_aux.get_instance()
            temporal = ''
            operador = ''
            val_der: Return = self.expresion_derecha.generar_c3d(scope)  

            if (self.tipo_operacion == "!"):  
                operador = '!'
                temporal = generador.add_temp()
                generador.add_exp(temporal, "",val_der.get_value(), operador)
                return Return(temporal, TipoEnum.BOOLEAN, True)
            elif (self.tipo_operacion == "&&"):
                val_izq: Return = self.expresion_izquierda.generar_c3d(scope)  
                operador = '&&'
                temporal = generador.add_temp()
                generador.add_exp(temporal, val_izq.get_value(),val_der.get_value(), operador)
                return Return(temporal, TipoEnum.BOOLEAN, True)
            elif (self.tipo_operacion == "||"):
                val_izq: Return = self.expresion_izquierda.generar_c3d(scope)
                operador = '||'
                temporal = generador.add_temp()
                generador.add_exp(temporal, val_izq.get_value(),val_der.get_value(), operador)
                return Return(temporal, TipoEnum.BOOLEAN, True)
 


           
