from Abstract.abstract import Abstract


class Funcion(Abstract):

    def __init__(self, linea, columna, id, tipo, parametros, sentancias):
        super().__init__(linea, columna)
        self.id = id
        self.tipo = tipo
        self.sentencias = sentancias
        self.parametros = parametros
        
    def __str__(self):
        return f"Funcion: {self.id}, Tipo: {self.tipo}, Parametros: {self.parametros}"

    
    def ejecutar(self, scope):
        result = self.sentencias.ejecutar(scope)
        return result
