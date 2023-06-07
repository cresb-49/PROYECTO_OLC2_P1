from Abstract.abstract import Abstract


class Declaracion(Abstract):
    def __init__(self, linea, columna, id, tipo, valor):
        super().__init__(linea, columna)
        self.id = id
        self.tipo = tipo
        self.valor = valor

    def __str__(self):
        return f"Declaracion: {self.id}, Tipo: {self.tipo}, Valor: {self.valor}"

    def ejecutar(self, scope):
        result = self.valor.ejecutar(scope)
        tipo_secundario = None
        scope.declarar_variable(
            self.id, result.valor, self.tipo, tipo_secundario, self.linea, self.columna)

    def graficar(self, scope, graphviz, subNameNode, padre):
        nume = graphviz.declaraciones.length + 1
        node = "nodo_" + subNameNode + "_" + nume
        decl = node + '[label = "<n>Declaracion"];'
        graphviz.declaraciones.push(decl)
        graphviz.relaciones.push((padre + ':n -> ' + node + ':n'))
