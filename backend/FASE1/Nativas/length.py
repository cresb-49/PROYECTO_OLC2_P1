from FASE1.Abstract.abstract import Abstract
from FASE1.Modulos.funcion_nativa import FuncionNativa
from FASE1.Symbol.tipoEnum import TipoEnum


class Length(Abstract):
    def __init__(self, resultado, linea, columna, acceder):
        super().__init__(resultado, linea, columna)
        self.acceder = acceder

    def __str__(self):
        return "length"

    def validar_tipos(self, tipo_exprecion):
        # si se trata de una suma debemos verificar que los dos tipos sean iguales y sean string o number
        if (tipo_exprecion == TipoEnum.STRING or tipo_exprecion == TipoEnum.ARRAY):
            # si la verificacion se cumple entonces pasamos del metodo
            return True
        else:
            self.resultado.add_error(
                'Semantico', f'Tipos no coinciden para la operacion length , Se esperaba String | Array y se recibio {tipo_exprecion}', self.linea, self.columna)
            return False

    def ejecutar(self, scope):
        #Verificar que solo venga un parametro
        if (len(self.acceder) == 1):
            expresion = self.acceder[0]
            # Enviar ha ejecutar la exprecion para obtener su diccionario
            ejecutar_expresion = expresion.ejecutar(scope)
            # enviar ha validar si se trata de un array o un string
            if(self.validar_tipos(ejecutar_expresion['tipo'])):
                #obtenemos el valor del el diccionario
                parametro = ejecutar_expresion['value']
                # mandamos ha ejecutar la funcion nativa con los valores recabados
                length = FuncionNativa.length(None, parametro)
                #retornamos el valor calculado por la funcion nativa
                return {"value": length, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            else:
                return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        else:
            self.resultado.add_error('Semantico', 'length(), no se puede ejecutar con mas de 1 parametro', self.linea, self.columna)
            return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        
    def graficar(self, graphviz, padre):
        # agregarmos el nombre del nodo (el de la operacion) y el nodo padre
        result = graphviz.add_nodo(".", padre)
        # mandmaos ha graficar os hijos
        self.acceder[0].graficar(graphviz, result)
        graphviz.add_nodo("length", result)

    def generar_c3d(self,scope):
        pass