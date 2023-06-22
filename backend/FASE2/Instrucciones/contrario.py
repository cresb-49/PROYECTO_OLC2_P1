from FASE2.Abstract.abstract import Abstract
from FASE2.Symbol.scope import Scope
from FASE2.Symbol.Exception import Excepcion


class Contrario(Abstract):

    def __init__(self, resultado, linea, columna, sentencias):
        super().__init__(resultado, linea, columna)
        self.sentencias: Abstract = sentencias
        # Variables de ayuda para la verificacion
        self.last_scope = None

    def __str__(self):
        return f"Contrario: resultado={self.resultado}, linea={self.linea}, columna={self.columna}, sentencias={self.sentencias}"

    def ejecutar(self, scope):
        self.last_scope = scope
        codigo_referencia = str(id(self))
        try:
            if self.sentencias != None:
                new_scope = Scope(scope)
                # Registramos el entorno utilizado
                self.resultado.agregar_entorno(codigo_referencia, new_scope)
                return self.sentencias.ejecutar(new_scope)
        except Exception:
            self.resultado.add_error(
                'Semantico', 'No se puede operar la sentencia existe un error anterior', self.linea, self.columna)

    def graficar(self, graphviz, padre):
        result = graphviz.add_nodo('else', padre)
        self.sentencias.graficar(graphviz, result)

    def generar_c3d(self, scope):
        if self.sentencias != None:
            self.sentencias.generar_c3d(scope)
        else:
            return  Excepcion("Semantico", f"Sentencias es None", self.linea, self.columna)