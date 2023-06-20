from Abstract.abstract import Abstract
from Modulos.funcion_nativa import FuncionNativa
from Symbol.tipoEnum import TipoEnum


class TypeOf(Abstract):
    def __init__(self, resultado, linea, columna, expreciones):
        super().__init__(resultado, linea, columna)
        self.expreciones = expreciones

    def __str__(self):
        return "TypeOf"

    def ejecutar(self, scope):

        # Verificar que solo venga un parametro
        if (len(self.expreciones) == 1):
            expresion = self.expreciones[0]
            # Enviar ha ejecutar la exprecion para obtener su diccionario
            ejecutarExpresion = expresion.ejecutar(scope)
            # calor del saparador de split
            tipo = ejecutarExpresion['tipo']
            tipo_secundario = ejecutarExpresion['tipo_secundario']

            if (tipo_secundario != None):
                # si el tipo secundario no es none entonces es un any y devolvemos el valor del tipo secundario
                return {"value": tipo_secundario, "tipo": TipoEnum.STRING, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            else:
                # si el tipo secundario es non entonces devolvemos el valor del tipo principal
                return {"value": tipo.value, "tipo": TipoEnum.STRING, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

        else:
            self.resultado.add_error(
                'Semantico', 'typeof(), no se puede ejecutar con mas de 1 parametro', self.linea, self.columna)
            return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        # agregarmos el nombre del nodo (el de la operacion) y el nodo padre
        result = graphviz.add_nodo("typeOf", padre)
        # mandmaos ha graficar os hijos
        self.expreciones[0].graficar(graphviz, result)

    def generar_c3d(self,scope):
        pass