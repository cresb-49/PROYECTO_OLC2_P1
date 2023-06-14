from Abstract.abstract import Abstract
from Modulos.funcion_nativa import FuncionNativa
from Symbol.tipoEnum import TipoEnum


class String(Abstract):
    def __init__(self, resultado, linea, columna, expreciones):
        super().__init__(resultado, linea, columna)
        self.expreciones = expreciones

    def __str__(self):
        return "String"

    def ejecutar(self, scope):
        # Verificar que solo venga un parametro
        if (len(self.expreciones) == 1):
            expresion = self.expreciones[0]
            # Enviar ha ejecutar la exprecion para obtener su diccionario
            ejecutarExpresion = expresion.ejecutar(scope)
            # calor del saparador de split
            parametro = ejecutarExpresion['value']
            # mandamos ha ejecutar la funcion nativa con los valores recabados
            parametroString = FuncionNativa.string(None, parametro)
            # retornamos un nuevo diccionario con la informacion del fixed
            return {"value": parametroString, "tipo": TipoEnum.STRING, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        else:
            self.resultado.add_error(
                'Semantico', 'String(), no se puede ejecutar con mas de 1 parametro', self.linea, self.columna)
            return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        # agregarmos el nombre del nodo (el de la operacion) y el nodo padre
        result = graphviz.add_nodo("String", padre)
        # mandmaos ha graficar os hijos
        self.expreciones[0].graficar(graphviz, result)
