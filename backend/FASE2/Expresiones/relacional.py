from FASE2.Abstract.abstract import Abstract
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Symbol.generador import Generador
from FASE2.Abstract.return__ import Return
from FASE2.Expresiones.logico import Logico
from FASE2.Symbol.Exception import Excepcion


class Relacional(Abstract):
    def __init__(self, resultado, linea, columna, expresion_izquierda, expresion_derecha, tipo_operacion):
        super().__init__(resultado, linea, columna)
        self.tipo = TipoEnum.BOOLEAN
        self.expresion_izquierda: Abstract = expresion_izquierda
        self.expresion_derecha: Abstract = expresion_derecha
        self.tipo_operacion = tipo_operacion
        # Guadado de los ultimos tipos ejecutados en el relacional
        self.last_scope = None
        self.last_exp_izq = None
        self.last_exp_der = None
        
    def __str__(self):
        return f"Relacional -> Tipo: {self.tipo}"
    
    def verificarTipos(self, val_izq, val_derecho):
        # extraemos el tipo de la exprecion izquierda de la op
        if (val_izq == None or val_derecho == None):
            return False
        tipo_exprecion_izquierda = val_izq["tipo"]
        tipo_exprecion_der = val_derecho["tipo"]
        if (tipo_exprecion_izquierda == tipo_exprecion_der and (tipo_exprecion_izquierda == TipoEnum.NUMBER or tipo_exprecion_izquierda == TipoEnum.STRING or tipo_exprecion_izquierda == TipoEnum.BOOLEAN)):
            # si se trata de una suma enviamos a validarla
            if tipo_exprecion_izquierda == TipoEnum.STRING:
                if self.tipo_operacion == '===' or self.tipo_operacion == '!==':
                    return True
                else:
                    concat = f'No puede realizar la operacion, string {self.tipo_operacion} string'
                    self.resultado.add_error(
                        'Semantico', concat, self.linea, self.columna)
                    print(concat)
                    return False
            elif tipo_exprecion_izquierda == TipoEnum.BOOLEAN:
                if self.tipo_operacion == '===' or self.tipo_operacion == '!==':
                    return True
                else:
                    concat = f'No puede realizar la operacion, boolean {self.tipo_operacion} boolean'
                    self.resultado.add_error(
                        'Semantico', concat, self.linea, self.columna)
                    print(concat)
                    return False
            else:
                return True
        else:
            concat = f'Tipos no coinciden para la operacion, Se esperaba number {self.tipo_operacion} number o string {self.tipo_operacion} string y se recibio {tipo_exprecion_izquierda.value} {self.tipo_operacion} {tipo_exprecion_der.value}'
            self.resultado.add_error(
                'Semantico', concat, self.linea, self.columna)
            print(concat)
            return False

    def ejecutar(self, scope):
        self.last_scope = scope
        val_izquierdo = self.expresion_izquierda.ejecutar(scope)
        val_derecho = self.expresion_derecha.ejecutar(scope)
        self.last_exp_izq = val_izquierdo
        self.last_exp_der = val_derecho

        if (self.verificarTipos(val_izquierdo, val_derecho)):
            result = None
            if (self.tipo_operacion == "===" or self.tipo_operacion == "=="):
                return {"value": result, "tipo": TipoEnum.BOOLEAN, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == "!==" or self.tipo_operacion == "!="):
                return {"value": result, "tipo": TipoEnum.BOOLEAN, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == "<"):
                return {"value": result, "tipo": TipoEnum.BOOLEAN, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == ">"):
                return {"value": result, "tipo": TipoEnum.BOOLEAN, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == "<="):
                return {"value": result, "tipo": TipoEnum.BOOLEAN, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == ">="):
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
        generador.add_comment("Compilacion de exprecion Logica")

        val_izq: Abstract = self.expresion_izquierda;
        val_der: Abstract = self.expresion_derecha;
        
        tipos_recuperados1 = val_izq.ejecutar(scope)
        tipos_recuperados2 = val_der.ejecutar(scope)
        
        
        tipo_izq = tipos_recuperados1['tipo']
        tipo_der = tipos_recuperados2['tipo']
        
        print('Manejo operaciones realacionel')
        print(tipo_izq)
        print(tipo_der)
        
        
        # TODO: Realizar la validacion de tipos

        if (self.tipo_operacion == "===" or self.tipo_operacion == "!=="):
            if tipo_izq == TipoEnum.ANY:
                return self.operaciones_asociadas(tipo_izq, val_izq, val_der, generador, scope)
            else:
                return self.operaciones_asociadas(tipo_izq, val_izq, val_der, generador, scope)
        else:
            if tipo_izq == TipoEnum.NUMBER:
                return self.comparacion_number(val_izq, val_der, generador, scope)
            elif tipo_izq == TipoEnum.ANY:
                return self.operaciones_asociadas(tipo_izq, val_izq, val_der, generador, scope)
            else:
                return Excepcion("Semantico", f"No existe operacion para el tipo  {self.last_exp_izq['tipo'].value} desconocida", self.linea, self.columna)

    def operaciones_asociadas(self, tipo, val_izq, val_der, generador, scope):
        if tipo == TipoEnum.NUMBER:
            return self.comparacion_number(val_izq, val_der, generador, scope)
        elif tipo == TipoEnum.STRING:
            return self.comparacion_string(val_izq, val_der, generador, scope)
        elif tipo == TipoEnum.BOOLEAN:
            return self.comparacion_bool(val_izq, val_der, generador, scope)
        else:
            return Excepcion("Semantico", f"Operacion desconocida  {tipo.value} desconocida", self.linea, self.columna)

    def check_labels(self):
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        if self.true_lbl == '':
            self.true_lbl = generador.new_label()
        if self.false_lbl == '':
            self.false_lbl = generador.new_label()

    def comparacion_number(self, exp_izq: Abstract, exp_der: Abstract, generador: Generador, scope):
        val_izq: Return = exp_izq.generar_c3d(scope)
        val_der: Return = exp_der.generar_c3d(scope)
        true_label = generador.new_label()
        false_label = generador.new_label()

        if self.tipo_operacion == '===':
            generador.add_if(val_izq.get_value(),
                             val_der.get_value(), '==', true_label)
        elif self.tipo_operacion == '!==':
            generador.add_if(val_izq.get_value(),
                             val_der.get_value(), '!=', true_label)
        else:
            generador.add_if(
                val_izq.get_value(), val_der.get_value(), self.tipo_operacion, true_label)
        generador.add_goto(false_label)
        generador.add_comment('Fin de la exprecion relacional')
        generador.add_space()

        result = Return(None, TipoEnum.BOOLEAN, False, None)
        result.add_true_lbl(true_label[:])
        result.add_false_lbl(false_label[:])
        return result

    def comparacion_bool(self, exp_izq: Abstract, exp_der: Abstract, generador: Generador, scope):
        ret: Return = Return(None, TipoEnum.BOOLEAN, False, None)
        and1: Logico = Logico(self.resultado, self.linea,
                              self.columna, exp_izq, exp_der, '&&')
        not_izq = Logico(self.resultado, self.linea,
                         self.columna, None, exp_izq, '!')
        not_der = Logico(self.resultado, self.linea,
                         self.columna, None, exp_der, '!')
        and2: Logico = Logico(self.resultado, self.linea,
                              self.columna, not_izq, not_der, '&&')
        or1: Logico = Logico(self.resultado, self.linea,
                             self.columna, and1, and2, '||')

        if self.tipo_operacion == '===':
            result: Return = or1.generar_c3d(scope)
            for label in result.get_true_lbls():
                ret.add_true_lbl(label)
            for label in result.get_false_lbls():
                ret.add_false_lbl(label)
            generador.add_comment('Fin de la exprecion relacional')
            generador.add_space()
            return ret
        else:
            not_all: Logico = Logico(
                self.resultado, self.linea, self.columna, None, or1, '!')
            result: Return = not_all.generar_c3d(scope)
            for label in result.get_true_lbls():
                ret.add_true_lbl(label)
            for label in result.get_false_lbls():
                ret.add_false_lbl(label)
            generador.add_comment('Fin de la exprecion relacional')
            generador.add_space()
            return ret

    def comparacion_string(self, exp_izq: Abstract, exp_der: Abstract, generador: Generador, scope):
        val_izq: Return = exp_izq.generar_c3d(scope)
        val_der: Return = exp_der.generar_c3d(scope)
        generador.fcompare_string()
        param_temp = generador.add_temp()
        generador.add_exp(param_temp, 'P', scope.size, '+')
        generador.add_exp(param_temp, param_temp, '1', '+')
        generador.set_stack(param_temp, val_izq.get_value())

        generador.add_exp(param_temp, param_temp, '1', '+')
        generador.set_stack(param_temp, val_der.get_value())

        generador.new_env(scope.size)
        generador.call_fun("compareString")

        temp = generador.add_temp()
        generador.get_stack(temp, 'P')
        generador.ret_env(scope.size)

        true_label = generador.new_label()
        false_label = generador.new_label()

        generador.add_if(temp, self.getNum(), '==', true_label)
        generador.add_goto(false_label)

        generador.add_comment('Fin de la exprecion relacional')
        generador.add_space()

        result = Return(None, TipoEnum.BOOLEAN, False, None)
        result.add_true_lbl(true_label[:])
        result.add_false_lbl(false_label[:])
        return result

    def getNum(self):
        if self.tipo_operacion == '===':
            return '1'
        if self.tipo_operacion == '!==':
            return '0'
