from Abstract.abstract import Abstract


class Acceder(Abstract):
    def __init__(self, linea, columna, id):
        super().__init__(linea, columna)
        self.id = id
    
    def ejecutar(self, scope):
        recuperacion = scope.obtenerVariable(self.id)
        if (recuperacion == None):
            raise ValueError("La variable",self.identificador,"no existe, Linea: ",self.linea," ,Columna: ",self.columna)
        return recuperacion
        