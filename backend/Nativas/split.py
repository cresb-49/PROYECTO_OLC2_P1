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
        # ejecutamos el diccionario de la cade
        ejecutar = self.cadena.ejecutar(scope)
        
        if(self.verificarTipos(ejecutar)):
            #Enviar ha ejecutar la exprecion para obtener su diccionario
            ejecutarExpresion = self.expreciones.ejecutar(scope)
            if(self.verificarTipos(ejecutarExpresion)):
                value_id = ejecutar['value'] #valor del id al que se aplico split
                value_separador = ejecutarExpresion['value'] #calor del saparador de split
                #mandamos ha ejecutar la funcion nativa con los valores recabados
                split = FuncionNativa.hacer_split(None, value_id, value_separador)
                
                arrayTmp = []

                #ADJUNTAMOS TODOS LOS STRING GENERADOS a un array terporal
                for cadena in split:
                    arrayTmp.append({"value": cadena, "tipo": TipoEnum.STRING, "tipo_secundario": None, "linea": self.linea, "columna": self.columna})
                
                return {"value": arrayTmp, "tipo": TipoEnum.ARRAY, "tipo_secundario": TipoEnum.STRING.value, "linea": self.linea, "columna": self.columna} 
            else:
                return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}  
        else:
            return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        # agregarmos el nombre del nodo (el de la operacion) y el nodo padre
        result = graphviz.add_nodo("toLowerCase", padre)
        # mandmaos ha graficar el hijo (acceder)
        self.numero.graficar(graphviz, result)
