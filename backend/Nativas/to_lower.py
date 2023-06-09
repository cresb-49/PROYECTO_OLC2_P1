from Abstract.abstract import Abstract
from Modulos.funcion_nativa import FuncionNativa
from Symbol.tipoEnum import TipoEnum


class ToLowerCase(Abstract):

    def __init__(self, resultado, linea, columna, numero):
        super().__init__(resultado, linea, columna)
        self.numero = numero

    def __str__(self):
        return "Concat"

    def verificarTipos(self, val):
        # extremos el tipo de la variable
        tipo = val["tipo"]
        if (tipo == TipoEnum.STRING):
            return True
        else:
            concat = 'Error: Tipos no coinciden para la operacion toLowerCase(), Se esperaba String y recibio ' + tipo.value
            self.resultado.add_error(
                'Semantico', concat, self.linea, self.columna)
            return False

    def ejecutar(self, scope):
        # ejecutamos el diccionario
        ejecutar = self.numero.ejecutar(scope)
        # una vez traida la variable debemos verificar que se trata d eun string
        if(self.verificarTipos(ejecutar)):
            # mandmaos ha hacer concat sobre el atributo value
            toString = FuncionNativa.hacer_to_lower_case(None, ejecutar['value'])
            # retornamos un diccionario con la String en lower y el tipo String
            return {"value": toString, "tipo": TipoEnum.STRING, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        else:
             # print('Debuj-> Primitivo ->', self)
            return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}



    def graficar(self, scope, graphviz, subNameNode, padre):
        nume = graphviz.declaraciones.length + 1
        node = "nodo_" + subNameNode + "_" + nume
        decl = node + '[label = "<n>LowerCase"];'
        graphviz.declaraciones.push(decl)
        graphviz.relaciones.push((padre + ':n -> ' + node + ':n'))
