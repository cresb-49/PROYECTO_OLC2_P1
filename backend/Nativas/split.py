from Abstract.abstract import Abstract
from Modulos.funcion_nativa import FuncionNativa
from Symbol.tipoEnum import TipoEnum


class Split(Abstract):
    def __init__(self, resultado, linea, columna, cadena, expreciones):
        super().__init__(resultado, linea, columna)
        self.expreciones = expreciones
        self.cadena = cadena

    def __str__(self):
        return "Concat"

    def verificarTipos(self, val):
        # extremos el tipo de la variable
        tipo = val["tipo"]
        if (tipo == TipoEnum.STRING):
            return True
        else:
            concat = 'Error: Tipos no coinciden para la operacion split(), Se esperaba String y recibio ' + \
                tipo.value
            self.resultado.add_error(
                'Semantico', concat, self.linea, self.columna)
            return False

    def ejecutar(self, scope):
        print("xxxx"+self.expreciones)
        # ejecutamos el diccionario de la cade
        ejecutar = self.cadena.ejecutar(scope)
        
        if(self.verificarTipos(ejecutar)):
            pass
        # if len(results) > 0:
        #     base = results[0]['tipo']
        #     if all(base == exp['tipo'] for exp in results):
        #         return {"value": results, "tipo": self.tipo, "tipo_secundario": base.value, "linea": self.linea, "columna": self.columna}
        #     else:
        #         return {"value": results, "tipo": self.tipo, "tipo_secundario": TipoEnum.ANY.value, "linea": self.linea, "columna": self.columna}
        # else:
        #     return {"value": results, "tipo": self.tipo, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        # agregarmos el nombre del nodo (el de la operacion) y el nodo padre
        result = graphviz.add_nodo("toLowerCase", padre)
        # mandmaos ha graficar el hijo (acceder)
        self.numero.graficar(graphviz, result)
