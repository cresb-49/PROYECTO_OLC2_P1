from FASE2.Abstract.return__ import Return
from FASE2.Abstract.abstract import Abstract
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Symbol.generador import Generador
from FASE2.Symbol.Exception import Excepcion

class Logico(Abstract):
    def __init__(self, resultado, linea, columna, expresion_izquierda, expresion_derecha, tipo_operacion):
        super().__init__(resultado, linea, columna)
        self.expresion_izquierda: Abstract = expresion_izquierda
        self.expresion_derecha: Abstract = expresion_derecha
        self.tipo_operacion = tipo_operacion

    def __str__(self):
        return f"Resultado: {self.resultado}\nLínea: {self.linea}\nColumna: {self.columna}\nExpresión Izquierda: {self.expresion_izquierda}\nExpresión Derecha: {self.expresion_derecha}\nTipo de Operación: {self.tipo_operacion}"

    def verificarTipos(self, val_izq, val_derecho):
        if ((val_izq == None or val_derecho == None) and self.tipo_operacion != '!'):
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
        if self.expresion_izquierda != None:
            val_izq = self.expresion_izquierda.ejecutar(scope)
        else:
            val_izq = None
        if self.tipo_operacion == '!':
            val_derecho = self.expresion_derecha.ejecutar(scope)
            if (self.verificarTipos(val_izq, val_derecho)):
                result = not val_derecho['value']
                return {"value": result, "tipo": TipoEnum.BOOLEAN, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            else:
                return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        else:
            val_derecho = self.expresion_derecha.ejecutar(scope)
            if (self.verificarTipos(val_izq, val_derecho)):
                if (self.tipo_operacion == "&&"):
                    val_izquierdo = self.expresion_izquierda.ejecutar(scope)
                    val_derecho = self.expresion_derecha.ejecutar(scope)
                    result = val_izquierdo['value'] and val_derecho['value']
                    return {"value": result, "tipo": TipoEnum.BOOLEAN, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
                elif (self.tipo_operacion == "||"):
                    val_izquierdo = self.expresion_izquierda.ejecutar(scope)
                    val_derecho = self.expresion_derecha.ejecutar(scope)
                    result = val_izquierdo['value'] or val_derecho['value']
                    return {"value": result, "tipo": TipoEnum.BOOLEAN, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            else:
                return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        result = graphviz.add_nodo(self.tipo_operacion, padre)
        if self.tipo_operacion != "!":
            self.expresion_izquierda.graficar(graphviz, result)
        self.expresion_derecha.graficar(graphviz, result)

    def generar_c3d(self, scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        generador.add_comment('Compilacion de Exprecion Relacional')
        if self.tipo_operacion == "!":
            ret: Return = Return(None, TipoEnum.BOOLEAN, False, None)
            rigth = self.expresion_derecha.generar_c3d(scope)
            # Invertimos las lista de verdadero y falso
            for label in rigth.get_true_lbls():
                ret.add_false_lbl(label)
            for label in rigth.get_false_lbls():
                ret.add_true_lbl(label)
            return ret
        elif self.tipo_operacion == '&&':
            ret: Return = Return(None, TipoEnum.BOOLEAN, False, None)
            left: Return = self.expresion_izquierda.generar_c3d(scope)
            for label in left.get_true_lbls():
                generador.put_label(label)
            rigth: Return = self.expresion_derecha.generar_c3d(scope)
            # Asignacion de nueva estiquetas verdaderas - las etiquetas verdaderas del segundo son las de este nuevo
            for label in rigth.get_true_lbls():
                ret.list_true_lbls.append(label)
            # Asignacion de nueva estiquetas falsas - las etiquetas falsas del primero y el segundo
            for label in left.get_false_lbls():
                ret.add_false_lbl(label)
            for label in rigth.get_false_lbls():
                ret.add_false_lbl(label)
            return ret
        elif self.tipo_operacion == '||':
            ret: Return = Return(None, TipoEnum.BOOLEAN, False, None)
            left: Return = self.expresion_izquierda.generar_c3d(scope)
            for label in left.get_false_lbls():
                generador.put_label(label)
            rigth: Return = self.expresion_derecha.generar_c3d(scope)
            # Asignacion de nueva estiquetas verdaderas - las etiquetas verdaderas del segundo son las de este nuevo
            for label in left.get_true_lbls():
                ret.add_true_lbl(label)
            for label in rigth.get_true_lbls():
                ret.add_true_lbl(label)
            # Asignacion de nueva estiquetas falsas - las etiquetas falsas del primero y el segundo
            for label in rigth.get_false_lbls():
                ret.add_false_lbl(label)
            return ret
        else:
            return Excepcion("Semantico", f"Operacion logica  {self.tipo_operacion} desconocida", self.linea, self.columna)

    def check_labels(self):
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        if self.true_lbl == '':
            self.true_lbl = generador.new_label()
        if self.false_lbl == '':
            self.false_lbl = generador.new_label()
