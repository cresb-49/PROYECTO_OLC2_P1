from Abstract.abstract import Abstract
from Symbol.scope import Scope
from Symbol.tipoEnum import TipoEnum

"""
tipo_for = 1 -> for (let i = 0; i < 10; i++) , declaracion, condicion, exprecion
tipo_for = 2 -> for (let var of var) , declaracion, exprecion
"""


class Para(Abstract):
    def __init__(self, resultado,linea, columna, tipo_for, declaracion, condicion, expresion, sentencias):
        super().__init__(resultado,linea, columna)
        self.tipo_for = tipo_for
        self.declaracion = declaracion
        self.condicion = condicion
        self.expresion = expresion
        self.sentencias = sentencias

    def __str__(self):
        return f"Tipo -> Tipo for: {self.tipo_for}, Declaración: {self.declaracion}, Condición: {self.condicion}, Expresión: {self.expresion}, Sentencias: {self.sentencias}"

    def ejecutar(self, scope):
        if self.tipo_for == 1:
            print('Ejecutamos for tipo 1')
            #Iniciamos un scope apartado del entorno del for
            scope_declarado_for: Scope = Scope(scope)
            #Declramos la variable asociada al for dentro del scope scope_declarado_for 
            self.declaracion.ejecutar(scope_declarado_for)
            #Verificamos la exprecion condicional del for
            result = self.condicion.ejecutar(scope_declarado_for)
            print(result)
            if result != None:
                if result['tipo'] == TipoEnum.BOOLEAN:
                    result:bool = result['value']
                    try:
                        scope_temporal:Scope = Scope(scope_declarado_for)
                        self.sentencias.ejecutar(scope_temporal)
                        
                        self.expresion.ejecutar(scope_declarado_for)
                        print(self.expresion)
                        result = self.condicion.ejecutar(scope_declarado_for)
                        scope_declarado_for.imprimir()
                        
                    except Exception as e:
                        #Toma el error de exception
                        print("Error:", str(e))
                else:
                    print('No se puede ejecutar la sentencia porque la condicional no es booleana')
            else:
                print('No se puede ejecutar la sentencia hay un error anterior')
            #self.declaracion.ejecutar(scope_dentro_for)
            #self.sentencias.ejecutar(scope_dentro_for)
        else:
            print('Ejecutamos for tipo 2')
            #scope_dentro_for: Scope = Scope(scope)
            #self.declaracion.ejecutar(scope_dentro_for)
            #self.sentencias.ejecutar(scope_dentro_for)

    
    
    
    
    def graficar(self, scope, graphviz, subNameNode, padre):
        nume = graphviz.declaraciones.length + 1
        node = "nodo_" + subNameNode + "_" + nume
        decl = node + '[label = "<n>Para"];'
        graphviz.declaraciones.push(decl)
        graphviz.relaciones.push((padre + ':n -> ' + node + ':n'))
        self.sentencias.graficar(scope, graphviz, subNameNode, node)
