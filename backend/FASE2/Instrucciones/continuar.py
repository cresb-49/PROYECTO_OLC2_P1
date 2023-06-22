from FASE2.Abstract.abstract import Abstract
from FASE2.Symbol.generador import Generador


class Continuar(Abstract):
    def __init__(self, resultado, linea, columna):
        super().__init__(resultado, linea, columna)
        # Variables para el codigo 3 direcciones
        self.last_scope = None

    def __str__(self):
        return f"Continue -> linea: {self.linea} ,columna: {self.columna}"

    def ejecutar(self, scope):
        self.last_scope = scope

    def graficar(self, graphviz, padre):
        graphviz.add_nodo('continue', padre)

    def generar_c3d(self, scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        generador.add_comment('Inicio de compilacion de continue')
        result = scope.get_scope_continue_ref()
        print('debuj =>', result)
        if result.continue_label == '':
            continue_label = generador.new_label()
            result.continue_label = continue_label
        generador.add_goto(result.continue_label)
        generador.add_comment('Fin de compilacion de continue')
