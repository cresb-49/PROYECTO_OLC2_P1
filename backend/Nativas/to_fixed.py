from Abstract.abstract import Abstract
from Modulos.funcion_nativa import FuncionNativa
from Symbol.tipoEnum import TipoEnum


class ToFixed(Abstract):
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
            concat = f'Tipos no coinciden para la operacion toFixed(), Se esperaba String y recibio {tipo.value}'
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
                fixed = FuncionNativa.hacer_to_fixed(None, value_id, exponencial)
                #retornamos un nuevo diccionario con la informacion del fixed    
                return {"value": fixed, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna} 
            else:
                return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}  
        else:
            return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        # agregarmos el nombre del nodo (el de la operacion) y el nodo padre
        result = graphviz.add_nodo(".", padre)
        # mandmaos ha graficar os hijos
        self.numero.graficar(graphviz, result)
        node_fixed = graphviz.add_nodo("toFixed", result)
        self.expreciones.graficar(graphviz, node_fixed)
    
    def generar_c3d(self,scope):
        pass