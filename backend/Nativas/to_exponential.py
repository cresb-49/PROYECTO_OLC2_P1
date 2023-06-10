from Abstract.abstract import Abstract
from Modulos.funcion_nativa import FuncionNativa
from Symbol.tipoEnum import TipoEnum


class ToExponential(Abstract):
    def __init__(self, resultado, linea, columna, numero, expreciones):
        super().__init__(resultado, linea, columna)
        self.expreciones = expreciones
        self.numero = numero

    def __str__(self):
        return "Concat"

    def verificarTipos(self, val):
        # extremos el tipo de la variable
        tipo = val['tipo']
        if (tipo == TipoEnum.NUMBER):
            return True
        else:
            concat = 'Error: Tipos no coinciden para la operacion toFixed(), Se esperaba Number y recibio ' + \
                tipo.value
            self.resultado.add_error(
                'Semantico', concat, self.linea, self.columna)
            return False

    def ejecutar(self, scope):
        # ejecutamos el diccionario del numero
        ejecutar = self.numero.ejecutar(scope)
        if(self.verificarTipos(ejecutar)):
            #Enviar ha ejecutar la exprecion para obtener su diccionario
            ejecutarExpresion = self.expreciones.ejecutar(scope)
            if(self.verificarTipos(ejecutarExpresion)):
                value_id = ejecutar['value'] #valor del id al que se aplico split
                exponencial = ejecutarExpresion['value'] #calor del saparador de split
                #mandamos ha ejecutar la funcion nativa con los valores recabados
                exponential = FuncionNativa.hacer_to_exponential(None, value_id, exponencial)
                #retornamos un nuevo diccionario con la informacion del fixed    
                return {"value": exponential, "tipo": TipoEnum.STRING, "tipo_secundario": None, "linea": self.linea, "columna": self.columna} 
            else:
                return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}  
        else:
            return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        # agregarmos el nombre del nodo (el de la operacion) y el nodo padre
        result = graphviz.add_nodo("toFixed", padre)
        # mandmaos ha graficar os hijos
        self.numero.graficar(graphviz, result)
        self.expreciones.graficar(graphviz, result)