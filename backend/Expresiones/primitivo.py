from Abstract.abstract import Abstract


class Primitivo(Abstract):
    def __init__(self, resultado, linea, columna, tipo, valor):
        super().__init__(resultado, linea, columna)
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

    def graficar(self, graphviz, padre):
        graphviz.add_nodo(self.valor, padre)

    def generar_c3d(self,scope):
        pass