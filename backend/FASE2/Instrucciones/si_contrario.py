from FASE2.Abstract.abstract import Abstract
from FASE2.Abstract.return__ import Return
from FASE2.Symbol.scope import Scope
from FASE2.Symbol.generador import Generador
from FASE2.Symbol.tipoEnum import TipoEnum


class SiContrario(Abstract):

    def __init__(self, resultado, linea, columna, exprecion_condicion, codigo_true, codigo_false):
        super().__init__(resultado, linea, columna)
        self.exprecion_condicion: Abstract = exprecion_condicion
        self.sentencias_true: Abstract = codigo_true
        self.sentencias_false: Abstract = codigo_false
        # Codigo de ayuda
        self.last_scope = None
        self.last_scope1 = None
        self.last_scope2 = None
        self.last_result = None

    def __str__(self):
        return f"SiContrario: resultado={self.resultado}, linea={self.linea}, columna={self.columna}, exprecion_condicion={self.exprecion_condicion}, sentencias_true={self.sentencias_true}, sentencias_false={self.sentencias_false}"

    def ejecutar(self, scope):
        self.last_scope = scope
        codigo_referencia = str(id(self))
        result = self.exprecion_condicion.ejecutar(scope)
        self.last_result = result
        try:
            if result['tipo'] == TipoEnum.BOOLEAN:
                self.exect_code_true(codigo_referencia, scope)
                self.exect_code_false(codigo_referencia, scope)
            else:
                self.resultado.add_error(
                    'Semantico', 'Error el else if opera con una exprecion booleana', self.linea, self.columna)
        except Exception:
            self.resultado.add_error(
                'Semantico', 'No se puede operar la sentencia existe un error anterior', self.linea, self.columna)

    def exect_code_true(self, codigo_referencia, scope):
        print('Else if -> Verdadero')
        if self.sentencias_true != None:
            new_scope = Scope(scope)
            self.last_scope1 = new_scope
            # Registramos el entorno utilizado
            self.resultado.agregar_entorno(codigo_referencia, new_scope)
            return self.sentencias_true.ejecutar(new_scope)

    def exect_code_false(self, codigo_referencia, scope):
        print('Else if -> Falso')
        if self.sentencias_false != None:
            new_scope = Scope(scope)
            self.last_scope2 = new_scope
            # Registramos el entorno utilizado
            self.resultado.agregar_entorno(
                codigo_referencia, new_scope)
            return self.sentencias_false.ejecutar(new_scope)

    def graficar(self, graphviz, padre):
        result = graphviz.add_nodo('else if', padre)
        node_condition = graphviz.add_nodo('condicion', result)
        self.exprecion_condicion.graficar(graphviz, node_condition)
        if self.sentencias_true != None:
            ct = graphviz.add_nodo('true', result)
            self.sentencias_true.graficar(graphviz, ct)
        if self.sentencias_false != None:
            ct = graphviz.add_nodo('false', result)
            self.sentencias_false.graficar(graphviz, ct)

    def generar_c3d(self, scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        generador.add_comment("Compilacion de de sentencia if")
        exit_label = generador.new_label()
        res: Return = self.exprecion_condicion.generar_c3d(self.last_scope)
        for label in res.get_true_lbls():
            generador.put_label(label)
        # Sentencias verdaderas del else if
        if self.sentencias_true != None:
            self.sentencias_true.generar_c3d(self.last_scope1)
        generador.add_goto(exit_label)
        for label in res.get_false_lbls():
            generador.put_label(label)
        # Sentencias falsas del else if
        if self.sentencias_false != None:
            self.sentencias_false.generar_c3d(self.last_scope2)
        generador.put_label(exit_label)
