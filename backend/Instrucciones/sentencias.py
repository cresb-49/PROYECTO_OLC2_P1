from Abstract.abstract import Abstract


class Sentencias(Abstract):
    def __init__(self, linea, columna, intrucciones:list):
        super().__init__(linea, columna)
        self.intrucciones = intrucciones

    def ejecutar(self, scope):
        for instr in self.intrucciones:
            print(instr)
