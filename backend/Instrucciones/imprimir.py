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
                    concat = self.imprimir_array(resultado)
                elif (resultado['tipo'] == TipoEnum.STRUCT):
                    concat = self.imprimir_struct(resultado)
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
        return self.imprimir_array_recu(resultado).replace('\'', '').replace('\\', '').replace('\"', '')

    def imprimir_struct(self, resultado):
        # concat es la variable que alojara todos los string del struct
        concat = "{\n"
        # por cada uno de los elementos principales en el value (titulos de propiedades del struct)
        for parametro in resultado['value']:
            # adjuntar al concat el titulo del parametro "parametro" y el value del parametro
            if resultado['value'][parametro]['tipo'] == TipoEnum.ARRAY:
                concat = concat + ' ' + str(parametro) + ': ' + str(self.imprimir_array(resultado['value'][parametro])) + '\n'
            else:
                concat = concat + ' ' + str(parametro) + ': ' + str(resultado['value'][parametro]['value']) + '\n'
        return concat + "}"

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
        main = graphviz.add_nodo('print', padre)
        node_params = graphviz.add_nodo('params', main)
        for param in self.exprecion:
            param.graficar(graphviz,node_params)
        # self.exprecion.graficar(graphviz, padre)
        # graphviz.add_nodo(');', padre)
        pass
