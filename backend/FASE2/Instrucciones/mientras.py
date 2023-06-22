from FASE2.Abstract.abstract import Abstract
from FASE2.Abstract.return__ import Return
from FASE2.Symbol.generador import Generador
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Symbol.scope import Scope

from FASE2.Instrucciones.continuar import Continuar
from FASE2.Instrucciones.detener import Detener
from FASE2.Symbol.Exception import Excepcion


class Mientras(Abstract):
    def __init__(self, resultado, linea, columna, condicion, sentencias):
        super().__init__(resultado, linea, columna)
        self.condicion: Abstract = condicion
        self.sentencias: Abstract = sentencias
        # Variables de ayuda para generacion de codigo en 3 direcciones
        self.last_scope: Scope = None
        self.last_pre_scope_while: Scope = None
        self.last_inner_scope_while: Scope = None

    def __str__(self):
        return f"While -> Condición: {self.condicion}, Sentencias: {self.sentencias}"

    def ejecutar(self, scope):
        self.last_scope = scope
        codigo_referencia = str(id(self))
        result = self.condicion.ejecutar(scope)
        if result != None:
            if result['tipo'] == TipoEnum.BOOLEAN:
                try:
                    # Este while es generado como un intemediario para almacenar
                    # banderas y etiquetas que lo puede tener un while en concreto
                    # Este scope no se comparte con otro while a pesar que puede estar
                    # al mismo nivel que otro.
                    # Lo utilizamos para evitar ambiguedad en los while consecutivos
                    scope_referencia_while: Scope = Scope(scope)
                    self.last_pre_scope_while = scope_referencia_while
                    scope_temporal: Scope = Scope(scope_referencia_while)
                    self.last_inner_scope_while = scope_temporal
                    # Registramos el scope generado
                    self.resultado.agregar_entorno(
                        codigo_referencia, scope_temporal)
                    if self.sentencias != None:
                        resultado = self.sentencias.ejecutar(scope_temporal)
                        if isinstance(resultado, dict):
                            return resultado
                        elif isinstance(resultado, Continuar):
                            pass
                        elif isinstance(resultado, Detener):
                            pass
                except Exception as e:
                    # Toma el error de exception
                    print("Error:", str(e))
            else:
                self.resultado.add_error(
                    'Semantico', 'No se puede ejecutar la sentencia porque la condicional no es booleana', self.linea, self.columna)

        else:
            self.resultado.add_error(
                'Semantico', 'No se puede ejecutar la sentencia hay un error anterior', self.linea, self.columna)

    def graficar(self, graphviz, padre):
        pass

    def generar_c3d(self, scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        generador.add_comment('Compilacion de ciclo while')
        # Generacion de la etiqueta de inicio del cilo
        lable_init = generador.new_label()
        generador.put_label(lable_init)
        # Generacion del codigo intermedio de la condicional
        ret: Return = self.condicion.generar_c3d(scope)
        if (isinstance(ret, Excepcion)):
            return ret
        # Generacion del scope intermedio para alamcenar las etiquetas de manejo del ciclo
        pre_scope_while: Scope = Scope(scope)
        # Ingreso de las etiquetas para las sentencias de break y continue en la generacion de codigo intermedio
        for label in ret.get_false_lbls():
            pre_scope_while.add_break_label(label)
        pre_scope_while.admit_continue_label = True
        # En el while continue hace un salto a la condicional por esa
        # razon establecemos de una vez esta etiqueta, en el for hasta
        # que hay un continue se genera dicha label se genera, porque no pueden ser
        # declaradas las labels y no utilizarlas o tener los goto y no existan las
        # labels
        pre_scope_while.set_continue_label(lable_init)
        # Generamos un scope para las oepraciones del scope
        inner_scope_while: Scope = Scope(pre_scope_while)
        # Imprecion de la label de entrada al ciclo
        for label in ret.get_true_lbls():
            generador.put_label(label)
        if self.sentencias != None:
            generador.add_comment('Inicio de sentencias dentro del while')
            self.sentencias.generar_c3d(inner_scope_while)
            generador.add_comment('Fin de sentencias dentro del while')
        # Imprecion de la etiqueta de repeticion del ciclo
        generador.add_goto(lable_init)
        # Imprecion de las label de salida del ciclo
        for label in ret.get_false_lbls():
            generador.put_label(label)
        generador.add_comment('Fin compilacion de ciclo while')
