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
            #Enviar ha ejecutar la exprecion para obtener su diccionario
            ejecutarExpresion = self.expreciones.ejecutar(scope)
            parametro = ejecutarExpresion['value'] #calor del saparador de split
            #mandamos ha ejecutar la funcion nativa con los valores recabados
            parametroString = FuncionNativa.string(None, parametro)
            #retornamos un nuevo diccionario con la informacion del fixed    
            return {"value": parametroString, "tipo": TipoEnum.STRING, "tipo_secundario": None, "linea": self.linea, "columna": self.columna} 



    def graficar(self, graphviz, padre):
        # agregarmos el nombre del nodo (el de la operacion) y el nodo padre
        result = graphviz.add_nodo("toFixed", padre)
        # mandmaos ha graficar os hijos
        self.numero.graficar(graphviz, result)
        self.expreciones.graficar(graphviz, result)