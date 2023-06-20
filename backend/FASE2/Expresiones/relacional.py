from FASE2.Abstract.abstract import Abstract
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Symbol.generador import Generador
from FASE2.Abstract.return__ import Return


class Relacional(Abstract):
    def __init__(self, resultado, linea, columna, expresion_izquierda, expresion_derecha, tipo_operacion):
        super().__init__(resultado, linea, columna)
        self.expresion_izquierda = expresion_izquierda
        self.expresion_derecha = expresion_derecha
        self.tipo_operacion = tipo_operacion

    def verificarTipos(self, val_izq, val_derecho):
        # extraemos el tipo de la exprecion izquierda de la op
        if (val_izq == None or val_derecho == None):
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
            if (self.tipo_operacion == "===" or self.tipo_operacion == "=="):
                result = val_izquierdo['value'] == val_derecho['value']
                return {"value": result, "tipo": TipoEnum.BOOLEAN, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == "!==" or self.tipo_operacion == "!="):
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

    def generar_c3d(self, scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        # temporal = ''
        # operador = ''

        generador.add_comment("Compilacion de exprecion Relaciona o Logica")
        val_izq: Return = self.expresion_izquierda.generar_c3d(scope)
        val_der: Return = self.expresion_derecha.generar_c3d(scope)
        # Verificacion de las labels de salto
        self.check_labels()
        if (self.tipo_operacion == "===" or self.tipo_operacion == "!=="):
            if val_izq.get_tipo() == TipoEnum.NUMBER:
                return self.comparacion_number(val_izq, val_der, generador)
            elif val_izq.get_tipo() == TipoEnum.STRING:
                pass
            else:
                pass
        else:
            if val_izq.get_tipo() == TipoEnum.NUMBER:
                return self.comparacion_number(val_izq, val_der, generador)
            else:
                pass

    def check_labels(self):
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        if self.true_lbl == '':
            self.true_lbl = generador.new_label()
        if self.false_lbl == '':
            self.false_lbl = generador.new_label()

    def comparacion_number(self, val_izq: Return, val_der: Return, generador: Generador):
        if self.tipo_operacion == '===':
            generador.add_if(val_izq.get_value(),val_der.get_value(), '==', self.true_lbl)
        elif self.tipo_operacion == '!==':
            generador.add_if(val_izq.get_value(),val_der.get_value(), '!=', self.true_lbl)
        else:
            generador.add_if(val_izq.get_value(), val_der.get_value(), self.tipo_operacion, self.true_lbl)
        generador.add_goto(self.false_lbl)
        generador.add_comment('Fin de la exprecion relacional')
        generador.add_space()

        result = Return(None, TipoEnum.BOOLEAN, False, None)
        result.set_true_lbl(self.true_lbl)
        result.set_false_lbl(self.false_lbl)
        return result
