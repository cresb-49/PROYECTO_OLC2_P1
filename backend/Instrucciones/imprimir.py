from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum


class Imprimir(Abstract):
    def __init__(self, resultado, linea, columna, exprecion):
        super().__init__(resultado, linea, columna)
        self.exprecion = exprecion

    def __str__(self):
        return f"Print -> Expresión: {self.exprecion}"

    def ejecutar(self, scope):
        concat = ""
        for diccionario in self.exprecion:
            resultado = diccionario.ejecutar(scope)
            if (isinstance(resultado, dict)):
                # si el tipo de dato es un array entonces debemos imprimirlo como tal
                if (resultado['tipo'] == TipoEnum.ARRAY):
                    self.imprimir_array(resultado)
                # si no es un array solo imprimimos normal y mandamos ha guardar la imprecion en la consola
                else:
                    print_val = resultado['value'] if resultado['value'] != None else 'Null'
                    concat = concat + " " + str(print_val)

            else:
                print('Debuj imprimir -> ', resultado)
                self.resultado.add_error(
                    'Semantico', 'Hubo un error previo ha imprimir el valor.', self.linea, self.columna)
        self.resultado.consola.append(concat)
        print(concat)

    def imprimir_array(self, resultado):
        # mandamos ha guardar el string en la consola
        printHecho = self.imprimir_array_recu(resultado).replace('\'', '').replace('\\', '').replace('\"', '')
        self.resultado.consola.append(printHecho)
        print(printHecho)

    # crea un string de array imprimible, si un elemento del array es un array entonces se convierte en funcion recursiva
    def imprimir_array_recu(self, resultado):
        contenido = []
        concat = ""
        # por cada uno de los stings contenidos en el aray de resultado ajuntamos el value del strin al array
        for string in resultado['value']:
            if (string['tipo'] == TipoEnum.ARRAY):
                concat = self.imprimir_array_recu(string)
            else:
                concat = string['value']
            contenido.append(concat)
        return str(contenido)

    def graficar(self, graphviz, padre):
        graphviz.add_nodo('console.log(', padre)
        self.exprecion.graficar(graphviz, padre)
        graphviz.add_nodo(');', padre)
