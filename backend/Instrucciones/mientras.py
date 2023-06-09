from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum
from Symbol.scope import Scope


class Mientras(Abstract):
    def __init__(self, resultado, linea, columna, condicion, sentencias):
        super().__init__(resultado, linea, columna)
        self.condicion = condicion
        self.sentencias = sentencias

    def __str__(self):
        return f"While -> Condición: {self.condicion}, Sentencias: {self.sentencias}"

    def ejecutar(self, scope):
        result = self.condicion.ejecutar(scope)
        if result != None:
            if result['tipo'] == TipoEnum.BOOLEAN:
                try:
                    res: bool = result['value']
                    while res:
                        scope_temporal: Scope = Scope(scope)
                        if self.sentencias != None:
                            resultado = self.sentencias.ejecutar(
                                scope_temporal)
                            if isinstance(resultado, dict):
                                return resultado
                            self.condicion.ejecutar(scope)
                        r = self.condicion.ejecutar(scope)
                        res = r['value']
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
        graphviz.add_nodo('while', padre)
        graphviz.add_nodo('{', padre)
        if (self.sentencias != None):
            self.sentencias.graficar(graphviz, padre)
        graphviz.add_nodo('}', padre)
