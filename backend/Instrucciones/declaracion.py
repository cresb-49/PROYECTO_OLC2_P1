from Abstract.abstract import Abstract


class Declaracion(Abstract):
    def __init__(self, linea, columna, id, tipo, valor):
        super().__init__(linea, columna)
        self.id = id
        self.tipo = tipo
        self.valor = valor

    def __str__(self):
        return f"Declaracion: {self.id}, Tipo: {self.tipo}, Valor: {self.valor}"
    
    def ejecutar(self, scope):
        result = self.valor.ejecutar(scope)
        scope.declarar_variable(self.id, result.value, result.tipo)
