from FASE2.Abstract.abstract import Abstract
from FASE2.Symbol.generador import Generador


class Detener(Abstract):
    def __init__(self, resultado, linea, columna):
        super().__init__(resultado, linea, columna)
        # Variables para el codigo 3 direcciones
        self.last_scope = None

    def __str__(self):
        return f"Break -> linea: {self.linea} ,columna: {self.columna}"

    def ejecutar(self, scope) -> any:
        self.last_scope = scope

    def graficar(self, graphviz, padre):
        graphviz.add_nodo('break', padre)

    def generar_c3d(self, scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        generador.add_comment('Inicio de compilacion de break')
        result = scope.get_break_ref()
        for label in result:
            generador.add_goto(label)
        generador.add_comment('Fin de compilacion de break')
