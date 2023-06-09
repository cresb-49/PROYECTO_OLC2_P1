from Abstract.abstract import Abstract
from Modulos.funcion_nativa import FuncionNativa
from Symbol.tipoEnum import TipoEnum

class Concat(Abstract):
    def __init__(self, resultado,linea, columna,expreciones):
        super().__init__(resultado,linea, columna)
        self.expreciones = expreciones

    def __str__(self):
        return "Concat"

    def ejecutar(self, scope):
        print(self.expreciones)
   
        # if len(results) > 0:
        #     base = results[0]['tipo']
        #     if all(base == exp['tipo'] for exp in results):
        #         return {"value": results, "tipo": self.tipo, "tipo_secundario": base.value, "linea": self.linea, "columna": self.columna}
        #     else:
        #         return {"value": results, "tipo": self.tipo, "tipo_secundario": TipoEnum.ANY.value, "linea": self.linea, "columna": self.columna}
        # else:
        #     return {"value": results, "tipo": self.tipo, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        #agregarmos el nombre del nodo (el de la operacion) y el nodo padre
        result = graphviz.add_nodo("toLowerCase", padre)
        #mandmaos ha graficar el hijo (acceder)
        self.numero.graficar(graphviz, result)
