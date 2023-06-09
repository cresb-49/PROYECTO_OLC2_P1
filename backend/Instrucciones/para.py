from Abstract.abstract import Abstract
from Symbol.scope import Scope
from Symbol.tipoEnum import TipoEnum

from Instrucciones.declaracion import Declaracion
from Instrucciones.asignacion import Asignacion
from Expresiones.primitivo import Primitivo
from Expresiones.aritmetica import Aritmetica
from Expresiones.acceder import Acceder
from Expresiones.acceder_array import AccederArray
from Expresiones.arreglo import Arreglo
from Expresiones.relacional import Relacional

"""
tipo_for = 1 -> for (let i = 0; i < 10; i++) , declaracion, condicion, exprecion
tipo_for = 2 -> for (let var of var) , declaracion, exprecion
"""


class Para(Abstract):
    def __init__(self, resultado, linea, columna, tipo_for, declaracion, condicion, expresion, sentencias):
        super().__init__(resultado, linea, columna)
        self.tipo_for = tipo_for
        self.declaracion = declaracion
        self.condicion = condicion
        self.expresion = expresion
        self.sentencias = sentencias

    def __str__(self):
        attributes = []
        for attr, value in self.__dict__.items():
            attributes.append(f"{attr}: {type(value).__name__}={value}")
        return f"{type(self).__name__}: " + ", ".join(attributes)

    def ejecutar(self, scope):
        if self.tipo_for == 1:
            ##print('Ejecutamos for tipo 1')
            # Iniciamos un scope apartado del entorno del for
            scope_declarado_for: Scope = Scope(scope)
            # Declramos la variable asociada al for dentro del scope scope_declarado_for
            self.declaracion.ejecutar(scope_declarado_for)
            # Verificamos la exprecion condicional del for
            result = self.condicion.ejecutar(scope_declarado_for)
            if result != None:
                if result['tipo'] == TipoEnum.BOOLEAN:
                    try:
                        res: bool = result['value']
                        while res:
                            scope_temporal: Scope = Scope(scope_declarado_for)
                            if self.sentencias != None:
                                resultado = self.sentencias.ejecutar(
                                    scope_temporal)
                                if isinstance(resultado, dict):
                                    return resultado
                            self.expresion.ejecutar(scope_declarado_for)
                            r = self.condicion.ejecutar(scope_declarado_for)
                            res = r['value']
                    except Exception as e:
                        # Toma el error de exception
                        print("Error:", str(e))
                else:
                    self.resultado.add_error('Semantico', 'No se puede ejecutar la sentencia porque la condicional no es booleana', self.linea, self.columna)
                    
            else:
                self.resultado.add_error('Semantico', 'No se puede ejecutar la sentencia hay un error anterior', self.linea, self.columna)
        else:
            ##print('Ejecutamos for tipo 2')
            # Iniciamos un scope apartado del entorno del for
            scope_declarado_for: Scope = Scope(scope)
            # Declramos la variable asociada al for dentro del scope scope_declarado_for
            result_expresion = self.expresion.ejecutar(scope_declarado_for)
            if result_expresion['tipo'] == TipoEnum.STRING or result_expresion['tipo'] == TipoEnum.ARRAY:
                # Generamos variables de ayuda para el ciclo
                # Contadores de acceso
                literal: Primitivo = Primitivo(
                    self.resultado, self.linea, self.columna, TipoEnum.NUMBER, float(0))
                maximo: Primitivo = Primitivo(
                    self.resultado, self.linea, self.columna, TipoEnum.NUMBER, float(len(result_expresion['value'])))
                contador: Declaracion = Declaracion(
                    self.resultado, self.linea, self.columna, '$contfor', TipoEnum.NUMBER, None, literal)
                limite: Declaracion = Declaracion(
                    self.resultado, self.linea, self.columna, '$maxfor', TipoEnum.NUMBER, None, maximo)
                op1: Acceder = Acceder(
                    self.resultado, self.linea, self.columna, '$contfor')
                op2: Primitivo = Primitivo(
                    self.resultado, self.linea, self.columna, TipoEnum.NUMBER, float(1))
                operacion: Aritmetica = Aritmetica(
                    self.resultado, self.linea, self.columna, op1, op2, '+')
                incrementar_valor: Asignacion = Asignacion(
                    self.resultado, self.linea, self.columna, '$contfor', operacion)
                if result_expresion['tipo'] == TipoEnum.ARRAY:
                    ##print('for of de un array')
                    ##print("estoy asignando Array")
                    var_arreglo: Declaracion = Declaracion(
                        self.resultado, self.linea, self.columna, '$valoresfor', TipoEnum.ARRAY, TipoEnum.ANY.value, self.expresion)
                    var_arreglo.ejecutar(scope_declarado_for)
                else:
                    ##print('for of de un string')
                    lista = [caracter for caracter in result_expresion['value']]
                    arreglo_nuevo = []
                    for l in lista:
                        val: Primitivo = Primitivo(
                            self.resultado, self.linea, self.columna, TipoEnum.STRING, l)
                        arreglo_nuevo.append(val)
                    arr: Arreglo = Arreglo(
                        self.resultado, self.linea, self.columna, TipoEnum.ARRAY, None, arreglo_nuevo)
                    var_arreglo: Declaracion = Declaracion(
                        self.resultado, self.linea, self.columna, '$valoresfor', TipoEnum.ARRAY, TipoEnum.STRING.value, arr)
                    var_arreglo.ejecutar(scope_declarado_for)
                
                try:
                    self.declaracion.ejecutar(scope_declarado_for)
                    limite.ejecutar(scope_declarado_for)
                    contador.ejecutar(scope_declarado_for)

                    contador_for = Acceder(self.resultado, self.linea, self.columna, '$contfor')
                    maximo_for = Acceder(self.resultado, self.linea, self.columna, '$maxfor')
                    self.condicion = Relacional(self.resultado, self.linea, self.columna, contador_for, maximo_for, '<')
                    result = self.condicion.ejecutar(scope_declarado_for)
                    
                    name_var_for = self.declaracion.id
                    var_array = Acceder(self.resultado,self.linea,self.columna,'$valoresfor')
                    index_array = Acceder(self.resultado,self.linea,self.columna,'$contfor')
                    acceder_array = AccederArray(self.resultado,self.linea,self.columna,var_array,index_array);
                    asignacion = Asignacion(self.resultado,self.linea,self.columna,name_var_for,acceder_array)
                    
                    while result['value']:
                        ##print('debuj')
                        asignacion.ejecutar(scope_declarado_for)
                        scope_temporal: Scope = Scope(scope_declarado_for)
                        if self.sentencias != None:
                            resultado = self.sentencias.ejecutar(scope_temporal)
                            if isinstance(resultado, dict):
                                return resultado
                        #Ejecuciones de final de ciclo
                        incrementar_valor.ejecutar(scope_declarado_for)    
                        result = self.condicion.ejecutar(scope_declarado_for)
                    
                except Exception as e:
                    print("Error:", str(e))
                
            else:
                self.resultado.add_error('Semantico', 'Solo se permiten iteraciones de array y string', self.linea, self.columna)

    def graficar(self, graphviz, padre):
        if self.tipo_for == 1:
            graphviz.add_nodo('for', padre)
            graphviz.add_nodo('(', padre)
            self.declaracion.graficar(graphviz, padre)
            graphviz.add_nodo(';', padre)
            self.condicion.graficar(graphviz, padre)
            graphviz.add_nodo(';', padre)
            self.expresion.graficar(graphviz, padre)
            graphviz.add_nodo(')', padre)
            graphviz.add_nodo('{', padre)
            if (self.sentencias != None):
                self.sentencias.graficar(graphviz, padre)
            graphviz.add_nodo('}', padre)
        else:
            graphviz.add_nodo('for', padre)
            graphviz.add_nodo('(', padre)
            graphviz.add_nodo(')', padre)
            graphviz.add_nodo('{', padre)
            if (self.sentencias != None):
                self.sentencias.graficar(graphviz, padre)
            graphviz.add_nodo('}', padre)
