from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum


class Imprimir(Abstract):
    def __init__(self, resultado, linea, columna, exprecion):
        super().__init__(resultado, linea, columna)
        self.exprecion = exprecion

    def __str__(self):
        return f"Print -> Expresión: {self.exprecion}"

    def ejecutar(self, scope):
        
        for diccionario in self.exprecion:
            resultado = diccionario.ejecutar(scope)
            #print(self.exprecion)
            if (isinstance(resultado, dict)):
                #si el tipo de dato es un array entonces debemos imprimirlo como tal
                if (resultado['tipo'] == TipoEnum.ARRAY):
                    self.imprimir_array(resultado)
                #si no es un array solo imprimimos normal y mandamos ha guardar la imprecion en la consola
                # elif (resultado['tipo'] == TipoEnum.ERROR):
                #     print(resultado['value'])
                #     self.resultado.consola.append(resultado['value'])
                else:
                    print_val = resultado['value'] if resultado['value'] != None else 'Null'
                    print(print_val)
                    self.resultado.consola.append(print_val)
            else:
                print('Debuj imprimir -> ',resultado)
                self.resultado.add_error('Semantico', 'Hubo un error previo ha imprimir el valor.', self.linea, self.columna)

    # imprime un array en un formato correcto
    def imprimir_array(self, resultado):
        contenido = []
        #por cada uno de los stings contenidos en el aray de resultado ajuntamos el value del strin al array
        for string in resultado['value']:
            contenido.append(string['value'])
        #mandamos ha guardar el string en la consola
        self.resultado.consola.append(str(contenido))
        print(str(contenido))

    def graficar(self, graphviz, padre):
        graphviz.add_nodo('console.log(', padre)
        self.exprecion.graficar(graphviz, padre)
        graphviz.add_nodo(');', padre)
