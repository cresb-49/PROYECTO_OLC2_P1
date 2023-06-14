from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum


class Asignacion(Abstract):
    def __init__(self, resultado, linea, columna, id, valor):
        super().__init__(resultado, linea, columna)
        self.id = id
        self.valor = valor

    def __str__(self):
        return f"Asignacion: {self.id}, Valor: {self.valor}"

    def ejecutar(self, scope):
        # Ejecutamos lo que vamos a asignar a la variable
        result_exprecion = self.valor.ejecutar(scope)
        # Buscamos la variable en el entorno/scope
        variable_recuperada = scope.obtener_variable(self.id)
        if variable_recuperada != None:
            # Verificamos una variable any ya que a esta le debemos cambiar su tipo secundario
            if variable_recuperada.tipo == TipoEnum.ANY:
                variable_recuperada.tipo_secundario = result_exprecion['tipo'].value
                variable_recuperada.valor = result_exprecion['value']
            else:
                # Verificamos que la variable recuperada coincida en tipo como es resultado de la exprecio
                if variable_recuperada.tipo == result_exprecion['tipo']:
                    variable_recuperada.valor = result_exprecion['value']
                else:
                    concat = f"No se puede asignar un: {result_exprecion['tipo'].value}, a la variable: {self.id}: {variable_recuperada.tipo.value} , linea: {self.linea}, columna: {self.columna}"
                    self.resultado.add_error(
                        'Semantico', concat, self.linea, self.columna)
        else:
            concat = 'No se puede encontrar la variable: ', self.id, ', linea: ', self.linea, ', columna: ', self.columna
            self.resultado.add_error(
                'Semantico', concat, self.linea, self.columna)

    def graficar(self, graphviz, padre):
        igual = graphviz.add_nodo('=', padre)
        graphviz.add_nodo(self.id, igual)
        self.valor.graficar(graphviz, igual)
        