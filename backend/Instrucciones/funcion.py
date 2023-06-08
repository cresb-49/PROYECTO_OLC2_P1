from Abstract.abstract import Abstract


class Funcion(Abstract):

    def __init__(self, resultado,linea, columna, id, tipo, parametros, sentancias):
        super().__init__(resultado,linea, columna)
        self.id = id
        self.tipo = tipo
        self.sentencias = sentancias
        self.parametros = parametros

    def __str__(self):
        return f"Funcion: {self.id}, Tipo: {self.tipo}, Parametros: {self.parametros}"

    def ejecutar(self, scope):
        result = self.sentencias.ejecutar(scope)
        return result

    def graficar(self, scope, graphviz, subNameNode, padre):
        # El codigo codigoReferencia no esta implementado
        # subName = self.codigoReferencia()
        node = "nodo_"+subNameNode+"_"+"0"
        # Array tipos no exite en esta implementacion...debera remplazarse por un metodo
        arrayTipos = ""
        # tipoString es un objeto pero no exite en esta implementacion...debera remplazarse por un objeto
        tipoString = ""
        decl = node+'[label = "<n>'+arrayTipos[self.tipo] + \
            ':'+self.id+'('+arrayTipos+')"];'
        graphviz.declaraciones.push("node [shape=record,width=.1,height=.1];")
        graphviz.declaraciones.push(decl)
        self.sentencias.graficar(scope, graphviz, subNameNode, node)
