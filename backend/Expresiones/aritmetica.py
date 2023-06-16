from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum
from Symbol.generador import Generador
from Abstract.return__ import Return


class Aritmetica(Abstract):
    def __init__(self, resultado, linea, columna, expresion_izquierda, expresion_derecha, tipo_operacion):
        super().__init__(resultado, linea, columna)
        self.expresion_izquierda = expresion_izquierda
        self.expresion_derecha = expresion_derecha
        self.tipo_operacion = tipo_operacion

    def verificarTipos(self, val_izquierdo, val_derecho):

        if(val_izquierdo == None or val_derecho == None):
            return False

        # extraemos el tipo de la exprecion izquierda de la op
        tipo_exprecion_izquierda = val_izquierdo["tipo"]
        # extraemos el tipo de la exprecion derecha de la op
        tipo_exprecion_der = val_derecho["tipo"]

        # print('debuj val izquierdo -> ',val_izquierdo)
        # print('debuj val derecho -> ',val_derecho)

        # extraemos el tipo de operacion que se quiere realizar
        tipo_operacion = self.tipo_operacion

        if (tipo_operacion == "+"):
            # si se trata de una suma enviamos a validarla
            return self.validar_suma(tipo_exprecion_izquierda, tipo_exprecion_der)
        else:
            return self.validar_otrasOperaciones(tipo_exprecion_izquierda, tipo_exprecion_der)

    def validar_suma(self, tipo_exprecion_izquierda, tipo_exprecion_der):
        # si se trata de una suma debemos verificar que los dos tipos sean iguales y sean string o number
        if (tipo_exprecion_izquierda == tipo_exprecion_der and (tipo_exprecion_izquierda == TipoEnum.NUMBER or tipo_exprecion_izquierda == TipoEnum.STRING)):
            # si la verificacion se cumple entonces pasamos del metodo
            return True
        else:
            self.resultado.add_error(
                'Semantico', f'Tipos no coinciden para la operacion {self.tipo_operacion} , Se esperaba number {self.tipo_operacion} number | string {self.tipo_operacion} string y se recibio {tipo_exprecion_izquierda.value} {self.tipo_operacion} {tipo_exprecion_der.value}', self.linea, self.columna)
            return False

    def validar_otrasOperaciones(self, tipo_exprecion_izquierda, tipo_exprecion_der):
        # si se trata de una operacion que no es una suma debemos verificar que los dos tipos sean iguales y number
        if (tipo_exprecion_izquierda == tipo_exprecion_der and (tipo_exprecion_izquierda == TipoEnum.NUMBER)):
            # si la verificacion se cumple entonces pasamos del metodo
            return True
        else:
            concat = f'Tipos no coinciden para la operacion {self.tipo_operacion}, Se esperaba number {self.tipo_operacion} number o string {self.tipo_operacion} string y se recibio {tipo_exprecion_izquierda.value} {self.tipo_operacion} {tipo_exprecion_der.value}'
            self.resultado.add_error(
                'Semantico', concat, self.linea, self.columna)

            return False

    def ejecutar(self, scope):

        val_izquierdo = self.expresion_izquierda.ejecutar(scope)
        val_derecho = self.expresion_derecha.ejecutar(scope)

        # print('Debuj-> Aritmetica -> tipo_operacion: ',self.tipo_operacion)
        # print('Debuj-> Aritmetica -> Izquierdo: ',val_izquierdo)
        # print('Debuj-> Aritmetica -> Derecho: ',val_derecho)

        if (self.verificarTipos(val_izquierdo, val_derecho)):
            if (self.tipo_operacion == "+"):
                result = val_izquierdo['value'] + val_derecho['value']
                return {"value": result, "tipo": val_izquierdo['tipo'], "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == "-"):
                result = val_izquierdo['value'] - val_derecho['value']
                return {"value": result, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == "*"):
                result = val_izquierdo['value'] * val_derecho['value']
                return {"value": result, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == "/"):
                if val_derecho == 0:
                    raise ValueError('Error: Divicion entre 0',
                                     'linea:', self.linea, 'columna', self.columna)
                result = val_izquierdo['value'] / val_derecho['value']
                return {"value": result, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == "%"):
                result = val_izquierdo['value'] % val_derecho['value']
                return {"value": result, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == "^"):
                result = val_izquierdo['value'] ** val_derecho['value']
                return {"value": result, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        else:
            # print('Debuj-> Primitivo ->', self)
            return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        result = graphviz.add_nodo(self.tipo_operacion, padre)
        self.expresion_izquierda.graficar(graphviz, result)
        self.expresion_izquierda.graficar(graphviz, result)

    def generar_c3d(self, scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        temporal = ''
        operador = ''

        # Al ejecutar obtenemos los tipos de los datos automaticamanete, 
        # no debemos realizar verificaciones porque ya el interprete hizo lo necesario
        val_izquierdo = self.expresion_izquierda.ejecutar(scope)
        val_derecho = self.expresion_derecha.ejecutar(scope)
        
        #Recuperamos los valores
        val_izq: Return = self.expresion_izquierda.generar_c3d(scope)
        val_der: Return = self.expresion_derecha.generar_c3d(scope)

        print('val_izquierdo',val_izquierdo)
        print('val_derecho',val_derecho)
        
        # TODO: Falta por implementar operaciones
        if (self.tipo_operacion == "+"):
            operador = '+'
            temporal = generador.add_temp()
            generador.add_exp(temporal, val_izq.get_value(),val_der.get_value(), operador)
            return Return(temporal, val_izquierdo['tipo'], True)
        elif (self.tipo_operacion == "-"):
            operador = '-'
            temporal = generador.add_temp()
            generador.add_exp(temporal, val_izq.get_value(),val_der.get_value(), operador)
            return Return(temporal, val_izquierdo['tipo'], True)
        elif (self.tipo_operacion == "*"):
            operador = '*'
            temporal = generador.add_temp()
            generador.add_exp(temporal, val_izq.get_value(),val_der.get_value(), operador)
            return Return(temporal, val_izquierdo['tipo'], True)
        elif (self.tipo_operacion == "/"):
            operador = '/'
            temporal = generador.add_temp()
            generador.add_exp(temporal, val_izq.get_value(),val_der.get_value(), operador)
            return Return(temporal, val_izquierdo['tipo'], True)
        elif (self.tipo_operacion == "%"):
            operador = '%'
            temporal = generador.add_temp()
            generador.add_exp(temporal, val_izq.get_value(),val_der.get_value(), operador)
            return Return(temporal, val_izquierdo['tipo'], True)
        elif (self.tipo_operacion == "^"):
            operador = '^'
            temporal = generador.add_temp()
            generador.add_exp(temporal, val_izq.get_value(),val_der.get_value(), operador)
            return Return(temporal, val_izquierdo['tipo'], True)
