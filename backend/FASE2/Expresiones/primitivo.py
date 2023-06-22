from FASE2.Abstract.abstract import Abstract
from FASE2.Symbol.generador import Generador
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Abstract.return__ import Return


class Primitivo(Abstract):
    def __init__(self, resultado, linea, columna, tipo, valor):
        super().__init__(resultado, linea, columna)
        self.tipo = tipo
        self.valor = valor

    def __str__(self):
        return f"Primitivo -> Tipo: {self.tipo}, Valor: {self.valor}"

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

    def generar_c3d(self, scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()

        if self.tipo == TipoEnum.BOOLEAN:

            result = Return(self.valor, self.tipo, False, None)
            true_label = generador.new_label()
            false_label = generador.new_label()

            if self.valor:
                generador.add_goto(true_label)
                generador.add_comment('goto para evitar error de go')
                generador.add_goto(false_label)
            else:
                generador.add_goto(false_label)
                generador.add_comment('goto para evitar error de go')
                generador.add_goto(true_label)

            result.add_true_lbl(true_label)
            result.add_false_lbl(false_label)

            return result

        elif self.tipo == TipoEnum.STRING:
            temporal = generador.add_temp()
            generador.add_asig(temporal, 'H')
            for char in str(self.valor):
                generador.set_heap('H', ord(char))
                generador.next_heap()
            generador.set_heap('H', -1)
            generador.next_heap()
            return Return(temporal, self.tipo, True, None)
        else:
            return Return(str(self.valor), self.tipo, False, None)
