from Abstract.abstract import Abstract
from Symbol.scope import Scope
from Symbol.tipoEnum import TipoEnum


class Si(Abstract):
    def __init__(self, resultado, linea, columna, exprecion, sentencias, _else):
        super().__init__(resultado, linea, columna)
        self.exprecion = exprecion
        self.sentencias = sentencias
        self._else = _else

    def __str__(self):
        return f"If -> Expresión: {self.exprecion}, Sentencias: {self.sentencias}, Else: {self._else}"

    def ejecutar(self, scope):
        result = self.exprecion.ejecutar(scope)
        try:
            if result['tipo'] == TipoEnum.BOOLEAN:
                if result['value']:
                    print('If -> Verdadero')
                    if self.sentencias != None:
                        new_scope = Scope(scope)
                        return self.sentencias.ejecutar(new_scope)
                else:
                    print('If -> Falso')
                    if self._else != None:
                        new_scope = Scope(scope)
                        return self._else.ejecutar(new_scope)
            else:
                print('Error el if opera con una exprecion booleana')
        except Exception:
            self.resultado.add_error(
                'Semantico', 'No se puede operar la sentencia existe un error anterior', self.linea, self.columna)

    def graficar(self, graphviz, padre):
        result = graphviz.add_nodo('if', padre)
        if self.exprecion != None:
            ct = graphviz.add_nodo('condition true', result)
            self.exprecion.graficar(graphviz, ct)
        if self._else != None:
            cf = graphviz.add_nodo('condition false', result)
            self._else.graficar(graphviz, cf)
