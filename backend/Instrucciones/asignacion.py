from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum


class Asignacion(Abstract):
    def __init__(self, linea, columna, id, valor):
        super().__init__(linea, columna)
        self.id = id
        self.valor = valor

    def __str__(self):
        return f"Asignacion: {self.id}, Valor: {self.valor}"

    def ejecutar(self, scope):
        #Ejecutamos lo que vamos a asignar a la variable
        result_exprecion = self.valor.ejecutar(scope)
        #Buscamos la variable en el entorno/scope
        variable_recuperada = scope.obtener_variable(self.id)
        if variable_recuperada != None:
            #Verificamos una variable any ya que a esta le debemos cambiar su tipo secundario
            if variable_recuperada.tipo == TipoEnum.ANY:
                variable_recuperada.tipo_secundario = result_exprecion['tipo'].value
                variable_recuperada.valor = result_exprecion['value']
            else:
                # Verificamos que la variable recuperada coincida en tipo como es resultado de la exprecio
                if variable_recuperada.tipo == result_exprecion['tipo']:
                    variable_recuperada.valor = result_exprecion['value']
                else:
                    print('No se puede asignar un:', result_exprecion['tipo'].value, ', a la variable ->', self.id,
                          ':', variable_recuperada.tipo.value, ', linea: ', self.linea, ', columna: ', self.columna)
        else:
            print('No se puede encontrar la variable: ', self.id,
                  ', linea: ', self.linea, ', columna: ', self.columna)

    def graficar(self, scope, graphviz, subNameNode, padre):
        nume = graphviz.declaraciones.length + 1
        node = "nodo_" + subNameNode + "_" + nume
        decl = node + '[label = "<n>Asignacion"];'
        graphviz.declaraciones.push(decl)
        graphviz.relaciones.push((padre + ':n -> ' + node + ':n'))
        nume2 = graphviz.declaraciones.length + 1
        node2 = "nodo_" + subNameNode + "_" + nume2
        decl2 = node2 + '[label = "<n>Exprecion"];'
        graphviz.declaraciones.push(decl2)
        graphviz.relaciones.push((node + ':n -> ' + node2 + ':n'))
