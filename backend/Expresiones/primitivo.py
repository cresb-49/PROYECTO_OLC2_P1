from Abstract.abstract import Abstract


class Primitivo(Abstract):
    def __init__(self, linea, columna, tipo, valor):
        super().__init__(linea, columna)
        self.tipo = tipo
        self.valor = valor

    def __str__(self):
        return f"Tipo: {self.tipo}, Valor: {self.valor}"

    def ejecutar(self, scope):
        """
        Ejecuta la función y retorna un diccionario con los siguientes valores:

        - "value": El valor del primitivo.
        - "tipo": El tipo del primitivo.
        - "tipo_secundario": Valor nulo (None) para esta función.
        - "linea": El número de línea donde se encuentra el primitivo.
        - "columna": El número de columna donde se encuentra el primitivo.
        """
        # print('Debuj-> Primitivo ->', self)
        return {"value": self.valor, "tipo": self.tipo, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, scope, graphviz, subNameNode, padre):
        num = graphviz.declaraciones.length + 1
        node = "nodo" + num + ' [label="<f0> ' + \
            self.tipo+' |<f1> ' + self.valor + '"];'
        graphviz.declaraciones.push(node)
        if (padre.length != 0):
            relacion = padre + ' -> ' + "nodo" + num
            graphviz.relaciones.push(relacion)
