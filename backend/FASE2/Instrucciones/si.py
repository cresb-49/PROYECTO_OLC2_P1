from FASE2.Abstract.abstract import Abstract
from FASE2.Abstract.return__ import Return
from FASE2.Symbol.scope import Scope
from FASE2.Symbol.generador import Generador
from FASE2.Symbol.tipoEnum import TipoEnum


class Si(Abstract):
    def __init__(self, resultado, linea, columna, exprecion, sentencias, _else):
        super().__init__(resultado, linea, columna)
        self.exprecion: Abstract = exprecion
        self.sentencias: Abstract = sentencias
        self._else: Abstract = _else
        # Parametos utilizados en para verificacion de informacion o ir a traer informacion
        self.last_scope1 = None
        self.last_scope2 = None
        self.last_scope3 = None
        self.last_result = None

    def __str__(self):
        return f"If -> Expresión: {self.exprecion}, Sentencias: {self.sentencias}, Else: {self._else}"

    def ejecutar(self, scope):
        self.last_scope1 = scope
        codigo_referencia = str(id(self))
        result = self.exprecion.ejecutar(scope)
        self.last_result = result
        try:
            if result['tipo'] == TipoEnum.BOOLEAN:
                if result['value']:
                    # print('If -> Verdadero')
                    if self.sentencias != None:
                        new_scope = Scope(scope)
                        self.last_scope2 = new_scope
                        # Registramos el entorno utilizado
                        self.resultado.agregar_entorno(
                            codigo_referencia, new_scope)
                        return self.sentencias.ejecutar(new_scope)
                else:
                    # print('If -> Falso')
                    if self._else != None:
                        new_scope = Scope(scope)
                        self.last_scope3 = new_scope
                        # Registramos el entorno utilizado
                        self.resultado.agregar_entorno(
                            codigo_referencia, new_scope)
                        return self._else.ejecutar(new_scope)
            else:
                self.resultado.add_error(
                    'Semantico', 'Error el if opera con una exprecion booleana', self.linea, self.columna)
        except Exception:
            self.resultado.add_error(
                'Semantico', 'No se puede operar la sentencia existe un error anterior', self.linea, self.columna)

    def graficar(self, graphviz, padre):
        result = graphviz.add_nodo('if', padre)
        node_condition = graphviz.add_nodo('condicion', result)
        self.exprecion.graficar(graphviz, node_condition)
        if self.sentencias != None:
            ct = graphviz.add_nodo('true', result)
            self.sentencias.graficar(graphviz, ct)
        if self._else != None:
            cf = graphviz.add_nodo('false', result)
            self._else.graficar(graphviz, cf)

    def generar_c3d(self, scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        generador.add_comment("Compilacion de de sentencia if")
        exit_label = generador.new_label()
        res: Return = self.exprecion.generar_c3d(scope)
        for label in res.get_true_lbls():
            generador.put_label(label)
        #Sentencias verdaderas del if
        if self.sentencias != None:
            self.sentencias.generar_c3d(scope)
        generador.add_goto(exit_label)
        for label in res.get_false_lbls():
            generador.put_label(label)
        #Sentencias falsas del if
        if self._else != None:
            self._else.generar_c3d(scope)
        generador.put_label(exit_label)
        generador.add_comment("fin compilacion de de sentencia if")
