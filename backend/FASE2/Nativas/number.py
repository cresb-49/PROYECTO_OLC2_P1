from FASE2.Abstract.abstract import Abstract
from FASE2.Modulos.funcion_nativa import FuncionNativa
from FASE2.Symbol.tipoEnum import TipoEnum


class Number(Abstract):
    def __init__(self, resultado, linea, columna, expreciones):
        super().__init__(resultado, linea, columna)
        self.expreciones = expreciones

    def __str__(self):
        return "Number"

    def ejecutar(self, scope):
        # Verificar que solo venga un parametro
        if (len(self.expreciones) == 1):
            expresion = self.expreciones[0]
            # Enviar ha ejecutar la exprecion para obtener su diccionario
            ejecutarExpresion = expresion.ejecutar(scope)
            # calor del saparador de split
            parametro = ejecutarExpresion['value']
            # mandamos ha ejecutar la funcion nativa con los valores recabados
            parametroNumber = FuncionNativa.number(None, parametro)
            # Si la respuesta del metodo es none entonces hubo un error de conversion
            if (parametroNumber == None):
                self.resultado.add_error(
                    'Semantico', 'Error al tratar de castear a formato Number', self.linea, self.columna)
                return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            
            # SI LA RESPUESTA NO ES NONE ENTONCES  DEVLVEMOS LA RESPUESTA
            return {"value": parametroNumber, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        else:
            self.resultado.add_error(
                'Semantico', 'Number(), no se puede ejecutar con mas de 1 parametro', self.linea, self.columna)
            return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        # agregarmos el nombre del nodo (el de la operacion) y el nodo padre
        result = graphviz.add_nodo("Number", padre)
        # mandmaos ha graficar os hijos
        self.expreciones[0].graficar(graphviz, result)

    def generar_c3d(self,scope):
        pass