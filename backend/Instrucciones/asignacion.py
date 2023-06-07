from Abstract.abstract import Abstract


class Asignacion(Abstract):
    def __init__(self, linea, columna, id, valor):
        super().__init__(linea, columna)
        self.id = id
        self.valor = valor

    def __str__(self):
        return f"Asignacion: {self.id}, Valor: {self.valor}"

    def ejecutar(self, scope):
        result = self.valor.ejecutar(scope)
        #tipo_secundario = None
        #modificar_variable(self.id, result.value, tipo_secundario):
