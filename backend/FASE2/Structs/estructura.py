from FASE2.Abstract.abstract import Abstract
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Symbol.scope import Scope
from FASE2.Symbol.Exception import Excepcion


class Estructura(Abstract):
    def __init__(self, resultado, linea, columna, id, composicion):
        super().__init__(resultado, linea, columna)
        self.id = id
        self.composicion = composicion
        self.configuracion = dict()

    def __str__(self):
        return f"Struct: id={self.id}, configuracion={self.configuracion}"

    def ejecutar(self, scope):
        pass

    def graficar(self, graphviz, padre):
        pass

    def generar_c3d(self, scope: Scope):
        # Calculo de las posiciones de los parametros de las estructuras
        params = 0
        for param in self.composicion:
            tmp = self.composicion[param]
            self.configuracion[param] = {
                'tipo': tmp['tipo'], 'tipo_secundario': tmp['tipo_secundario'], 'pos': params}
            params += 1
        # Declaracion del struct en el scope
        try:
            scope.declarar_estructura(self.id, self)
        except ValueError as e:
            self.resultado.add_error('Semantico', str(e), self.linea, self.columna)
            return Excepcion('Semantico', str(e), self.linea, self.columna)