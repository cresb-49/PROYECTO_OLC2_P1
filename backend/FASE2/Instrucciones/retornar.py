from FASE2.Abstract.abstract import Abstract
from FASE2.Abstract.return__ import Return
from FASE2.Symbol.generador import Generador
from FASE2.Symbol.scope import Scope


class Retornar(Abstract):
    def __init__(self, resultado, linea, columna, exprecion):
        super().__init__(resultado, linea, columna)
        self.exprecion: Abstract = exprecion

    def __str__(self):
        # return f"Return -> Expresión: {self.exprecion}"
        return f"Return -> linea: {self.linea} ,columna: {self.columna}"

    def ejecutar(self, scope):
        if self.exprecion != None:
            valor = self.exprecion.ejecutar(scope)
            return valor
        else:
            return None

    def graficar(self, graphviz, padre):
        node_result = graphviz.add_nodo('return', padre)
        if self.exprecion != None:
            self.exprecion.graficar(graphviz, node_result)

    def generar_c3d(self, scope: Scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()

        # Buscamos las return labels
        lista_labels_return = scope.get_return_ref()
        print(lista_labels_return)

        result: Return = None
        if self.exprecion != None:
            result = self.exprecion.generar_c3d(scope)
        if result != None:
            if len(result.get_true_lbls()) == 0:
                generador.add_comment('Resultado a retorna en la funcion')
                generador.set_stack('P',result.get_value())
                for lable in lista_labels_return:
                    generador.add_goto(lable)    
                generador.add_comment('Fin del resultado a retornar')
            else:
                generador.add_comment('Resultado a retorna en la funcion')
                for labels in result.get_true_lbls():
                    generador.put_label(labels)
                generador.set_stack('P','1')
                for lable in lista_labels_return:
                    generador.add_goto(lable)
                for labels in result.get_false_lbls():
                    generador.put_label(labels)
                generador.set_stack('P','0')
                for lable in lista_labels_return:
                    generador.add_goto(lable)
                generador.add_comment('Fin del resultado a retornar')
        else:
            generador.add_comment('Resultado a retorna en la funcion')
            for lable in lista_labels_return:
                generador.add_goto(lable)
            generador.add_comment('Fin del resultado a retornar')
