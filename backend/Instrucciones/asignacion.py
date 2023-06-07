from Abstract.abstract import Abstract


class Asignacion(Abstract):
    def __init__(self, linea, columna, id, valor):
        super().__init__(linea, columna)
        self.id = id
        self.valor = valor

    def ejecutar(self, scope):
        result = self.valor.ejecutar(scope)
        #scope.modificar_variable(self.id, result.value, result.tipo)
