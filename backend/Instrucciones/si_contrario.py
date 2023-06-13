from Abstract.abstract import Abstract
from Symbol.scope import Scope
from Symbol.tipoEnum import TipoEnum


class SiContrario(Abstract):

    def __init__(self, resultado, linea, columna, exprecion_condicion, codigo_true, codigo_false):
        super().__init__(resultado, linea, columna)
        self.exprecion_condicion = exprecion_condicion
        self.sentencias_true = codigo_true
        self.sentencias_false = codigo_false

    def __str__(self):
        return f"SiContrario: resultado={self.resultado}, linea={self.linea}, columna={self.columna}, exprecion_condicion={self.exprecion_condicion}, sentencias_true={self.sentencias_true}, sentencias_false={self.sentencias_false}"

    def ejecutar(self, scope):
        codigo_referencia = str(id(self))
        result = self.exprecion_condicion.ejecutar(scope)
        try:
            if result['tipo'] == TipoEnum.BOOLEAN:
                if result['value']:
                    print('Else if -> Verdadero')
                    if self.sentencias_true != None:
                        new_scope = Scope(scope)
                        # Registramos el entorno utilizado
                        self.resultado.agregar_entorno(codigo_referencia, new_scope)
                        return self.sentencias_true.ejecutar(new_scope)
                else:
                    print('Else if -> Falso')
                    if self.sentencias_false != None:
                        new_scope = Scope(scope)
                        # Registramos el entorno utilizado
                        self.resultado.agregar_entorno(codigo_referencia, new_scope)
                        return self.sentencias_false.ejecutar(new_scope)
            else:
                self.resultado.add_error(
                    'Semantico', 'Error el else if opera con una exprecion booleana', self.linea, self.columna)
        except Exception:
            self.resultado.add_error(
                'Semantico', 'No se puede operar la sentencia existe un error anterior', self.linea, self.columna)

    def graficar(self, graphviz, padre):
        graphviz.add_nodo('else if', padre)
        graphviz.add_nodo('(', padre)
        if self.exprecion_condicion != None:
            self.exprecion_condicion.graficar(graphviz,padre)
        graphviz.add_nodo(')', padre)
        graphviz.add_nodo('{', padre)
        if self.sentencias_true != None:
            self.sentencias_true.graficar(graphviz,padre)
        graphviz.add_nodo('}', padre)
        if self.sentencias_false != None:
            self.sentencias_false.graficar(graphviz,padre)
        
