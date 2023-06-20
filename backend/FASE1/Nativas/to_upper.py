from FASE1.Abstract.abstract import Abstract
from FASE1.Modulos.funcion_nativa import FuncionNativa
from FASE1.Symbol.tipoEnum import TipoEnum


class ToUpperCase(Abstract):

    def __init__(self, resultado, linea, columna, numero):
        super().__init__(resultado, linea, columna)
        self.numero = numero

    def __str__(self):
        return "toUpperCase"

    def verificarTipos(self, val):
        # extremos el tipo de la variable
        tipo = val["tipo"]
        if (tipo == TipoEnum.STRING):
            return True
        else:
            concat = f'Tipos no coinciden para la operacion split(), Se esperaba String y recibio {tipo.value}'
            self.resultado.add_error(
                'Semantico', concat, self.linea, self.columna)
            return False

    def ejecutar(self, scope):
        # ejecutamos el diccionario
        ejecutar = self.numero.ejecutar(scope)
        # una vez traida la variable debemos verificar que se trata d eun string
        if(self.verificarTipos(ejecutar)):
            # mandmaos ha hacer concat sobre el atributo value
            toString = FuncionNativa.hacer_to_upper_case(None, ejecutar['value'])
            # retornamos un diccionario con la String en lower y el tipo String
            return {"value": toString, "tipo": TipoEnum.STRING, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        else:
             # print('Debuj-> Primitivo ->', self)
            return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}



    def graficar(self, graphviz, padre):
        #agregarmos el nombre del nodo (el de la operacion) y el nodo padre
        result = graphviz.add_nodo(".", padre)
        #mandmaos ha graficar el hijo (acceder)
        self.numero.graficar(graphviz, result)
        graphviz.add_nodo("toUpperCase", result)
    
    def generar_c3d(self,scope):
        pass