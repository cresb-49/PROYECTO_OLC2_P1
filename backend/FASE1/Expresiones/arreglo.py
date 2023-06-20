from FASE1.Abstract.abstract import Abstract
from FASE1.Symbol.tipoEnum import TipoEnum


class Arreglo(Abstract):
    def __init__(self, resultado, linea, columna, tipo, tipo_secundario, arreglo):
        super().__init__(resultado, linea, columna)
        self.tipo = tipo
        self.tipo_secundario = tipo_secundario
        self.arreglo = arreglo

    def ejecutar(self, scope):
        results = []
        for parte in self.arreglo:
            resultado = parte.ejecutar(scope)
            results.append(resultado)

        if len(results) > 0:
            base = results[0]['tipo']
            if all(base == exp['tipo'] for exp in results):
                tipo_secundario = base.value
                return {"value": results, "tipo": self.tipo, "tipo_secundario": tipo_secundario, "linea": self.linea, "columna": self.columna}
            else:
                return {"value": results, "tipo": self.tipo, "tipo_secundario": TipoEnum.ANY.value, "linea": self.linea, "columna": self.columna}
        else:
            return {"value": results, "tipo": self.tipo, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        node_padre = graphviz.add_nodo('[]', padre)
        for parte in self.arreglo:
            parte.graficar(graphviz, node_padre)

    def generar_c3d(self,scope):
        pass