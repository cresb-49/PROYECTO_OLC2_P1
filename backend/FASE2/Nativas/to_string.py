from FASE2.Abstract.abstract import Abstract
from FASE2.Modulos.funcion_nativa import FuncionNativa
from FASE2.Symbol.tipoEnum import TipoEnum


class ToString(Abstract):

    def __init__(self, resultado, linea, columna, numero):
        super().__init__(resultado, linea, columna)
        self.numero = numero

    def __str__(self):
        return "toString"

    def ejecutar(self, scope):
        # ejecutamos el diccionario
        ejecutar = self.numero.ejecutar(scope)
        # mandmaos ha hacer concat sobre el atributo value
        toString = FuncionNativa.hacer_to_string(None, ejecutar['value'])
        # retornamos un diccionario con la String realizada y el tipo String
        return {"value": toString, "tipo": TipoEnum.STRING, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        # agregarmos el nombre del nodo (el de la operacion) y el nodo padre
        result = graphviz.add_nodo(".", padre)
        # mandmaos ha graficar el hijo (acceder)
        self.numero.graficar(graphviz, result)
        graphviz.add_nodo("toString", result)

    def generar_c3d(self, scope):
        # ejecutamos el diccionario para poder obtener el tipo de dato que se desea convertir ha String
        ejecutar = self.numero.ejecutar(scope)
        if (ejecutar['tipo'] == TipoEnum.ARRAY):
            # convercion del valor a String
            valString = self.imprimir_array_recu(ejecutar)
        else:
            # convercion del valor a String
            valString = str(ejecutar['value'])

        
        # segun el tipo de la variable debemos
        print(f'----DEBUG----->{valString}')

    def imprimir_array_recu(self, resultado):
        contenido = []
        concat = ""
        # por cada uno de los stings contenidos en el aray de resultado ajuntamos el value del strin al array
        for string in resultado['value']:
            if (string['tipo'] == TipoEnum.ARRAY):
                concat = self.imprimir_array_recu(string)
            elif (string['tipo'] == TipoEnum.STRUCT):
                concat = self.imprimir_struct(string)
            elif (string['tipo'] == TipoEnum.STRING):
                concat = "\""+string['value']+"\""
            else:
                concat = string['value']
            contenido.append(concat)
        return str(contenido)
