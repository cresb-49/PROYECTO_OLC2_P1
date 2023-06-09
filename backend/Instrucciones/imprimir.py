from Abstract.abstract import Abstract


class Imprimir(Abstract):
    def __init__(self, resultado,linea, columna, exprecion):
        super().__init__(resultado,linea, columna)
        self.exprecion = exprecion

    def __str__(self):
        return f"Print -> Expresión: {self.exprecion}"

    def ejecutar(self, scope):
        resultado = self.exprecion.ejecutar(scope)

        if(isinstance(resultado, dict)):
            print(resultado['value'])
        else:
            print(resultado)
            self.resultado.add_error(
                'Semantico', 'Hbo un error previo ha imprimir el valor.', self.linea, self.columna)

    def graficar(self, graphviz, padre):
        graphviz.add_nodo('console.log(', padre)
        self.exprecion.graficar(graphviz,padre)
        graphviz.add_nodo(');', padre)
        
