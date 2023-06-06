from enum import Enum

##### ENUMS DE LA LOGICA ######


class OpcionOperacion(Enum):
    SUMA = 1
    RESTA = 2
    MUL = 3
    DIV = 4
    MOD = 5
    POT = 6


class OpcionLogica(Enum):
    AND = 0
    OR = 1
    NOT = 2


class TipoEnum(Enum):
    NUMBER = 0
    BOOLEAN = 1
    STRING = 2
    ANY = 3
    STRUCT = 4
    ERROR = 5


class OpcionRelacional(Enum):
    IGUAL = 0
    DIFERENTE = 1
    MENOR = 2
    MAYOR = 3
    MENOR_IGUAL = 4
    MAYOR_IGUAL = 5

##### CLASE TIPO ######


class Tipo():
    """
    Tipo de datos con los primitivos en enum, y un tipo secudario usado en any y struct
    """

    def __init__(self, tipo: TipoEnum, tipo_secundario):
        self.type = tipo
        self.tipo_secundario = tipo_secundario

    def get_tipo(self):
        return self.type

    def get_tipo_string(self):
        if (self.type == TipoEnum.NUMBER):
            return 'number'
        elif (self.type == TipoEnum.BOOLEAN):
            return 'boolean'
        elif (self.type == TipoEnum.STRING):
            return 'string'
        elif (self.type == TipoEnum.ANY):
            return 'any'
        elif (self.type == TipoEnum.STRUCT):
            return 'struct'
        elif (self.type == TipoEnum.ERROR):
            return 'error'

    def get_tipo_secundario(self):
        return self.tipo_secundario


class Simbolo:
    def __init__(self, valor, id_, tipo, linea, columna):
        self.valor = valor
        self.id = id_
        self.tipo = tipo
        self.linea = linea
        self.columna = columna


class Scope:
    def __init__(self, anterior) -> None:
        self.anterior = anterior
        self.variables = Variables()
        self.funciones = Funciones()

    def declarar_variable(self, identificador: str, valor: any, tipo: Tipo, linea, columna):
        try:
            self.variables.add(identificador, Simbolo(
                valor, identificador, tipo, linea, columna))
        except ValueError as error:
            print(f"Se produjo un error: {str(error)}")

    def modificar_variable(self, identificador: str, valor: any, tipo: Tipo):
        if self.variables.has(identificador):
            self.variables.update(identificador, valor, tipo)
        else:
            raise ValueError(
                "No se modificar la variable porque no existe en el scope")

    def obtener_variable(self, identificador: str) -> Simbolo | None:
        scope = self
        while (scope != None):
            if (scope.variables.has(identificador)):
                return scope.variables.get(identificador)
            scope = scope.anterior
        return None

    def declarar_funcion(self, identificador: str, funcion):
        try:
            self.funciones.add(identificador, funcion)
        except ValueError as error:
            print(f"Se produjo un error: {str(error)}")

    def obtener_funcion(self, identificador: str):
        scope = self
        while (scope != None):
            if (scope.funciones.has(identificador)):
                return scope.funciones.get(identificador)
            scope = scope.anterior
        return None


##### CLASE RETORNO ######


class Retorno():

    def __init__(self, value: any, tipo: Tipo):
        self.value = value
        self.tipo = tipo

##### CLASE EXPRECION ######


class Exprecion:
    def __init__(self, linea, columna):
        self.linea = linea
        self.columna = columna

    def ejecutar(self, scope: Scope) -> Retorno:
        print(scope)

    def graficar(self, scope, graphviz, padre):
        print(scope, graphviz, padre)
        return None

##### CLASE INSTRUCCION ######


class Instruccion:
    def __init__(self, linea, columna):
        self.linea = linea
        self.columna = columna

    # Funcion base se debe de sobreescibir para las demas clases heredadas
    def ejecutar(self, scope: Scope) -> any:
        print(scope)
        return None

    # Funcion base se debe de sobreescibir para las demas clases heredadas
    def graficar(self, scope, graphviz, padre) -> None:
        print(scope, graphviz, padre)
        return None

##### CLASE ACCEDER ######


class Acceder(Exprecion):
    def __init__(self, linea, columna, identificador):
        super().__init__(linea, columna)
        self.identificador = identificador

    def ejecutar(self, scope: Scope) -> Retorno:
        recuperacion = scope.obtenerVariable(self.identificador)
        if (recuperacion == None):
            raise ValueError("La variable \"" + self.identificador +
                             "\" no existe, Linea: " + self.linea + " ,Columna: " + self.columna)

        # TODO:establecer el tipo de retorno logica no hecha
        return Retorno(recuperacion.valor, None)

    def graficar(self, scope, graphviz, padre):
        num = graphviz.declaraciones.length + 1
        node = "nodo" + num + \
            ' [label="<f0> ID |<f1> ' + self.identificador + '"];'
        graphviz.declaraciones.push(node)
        if (padre.length != 0):
            relacion = padre + ' -> ' + "nodo" + num
            graphviz.relaciones.push(relacion)

##### CLASE LITERAL ######


class Literal(Exprecion):
    def __init__(self, linea, columna, valor, tipo: Tipo):
        super().__init__(linea, columna)
        self.valor = valor
        self.tipo = tipo

    def ejecutar(self, scope: Scope) -> Retorno:
        return Retorno(self.valor, self.tipo)

    def graficar(self, scope, graphviz, padre):
        num = graphviz.declaraciones.length + 1
        node = "nodo" + num + \
            ' [label="<f0> ' + Tipo.get_tipo_string() + \
            ' |<f1> ' + self.valor + '"];'
        graphviz.declaraciones.push(node)
        if (padre.length != 0):
            relacion = padre + ' -> ' + "nodo" + num
            graphviz.relaciones.push(relacion)

##### CLASE LITERAL ######


class Logica(Exprecion):
    def __init__(self, linea, columna, izquierda: Exprecion, derecha: Exprecion, tipo: OpcionLogica):
        super().__init__(linea, columna)
        self.valOperacion = ['&&', '||', '!']
        self.izquierda = izquierda
        self.derecha = derecha
        self.tipo = tipo

    def ejecutar(self, scope: Scope) -> Retorno:
        valor_izquierdo = self.izquierda.ejecutar(scope)
        valor_derecha = self.derecha.ejecutar(scope)

        if (self.tipo == OpcionLogica.NOT):
            if (valor_derecha.tipo.get_tipo() != TipoEnum.BOOLEAN):
                raise ValueError(
                    "Para realizar una operacion logica se necesita de un valor booleano al lado derecho ,Linea: "+self.linea+" ,Columna: "+self.columna)
        else:

            if (valor_izquierdo.tipo.get_tipo() != TipoEnum.BOOLEAN):
                raise ValueError(
                    "Para realizar una operacion logica se necesita de un valor booleano al lado izquierdo ,Linea: "+self.linea+" ,Columna: "+self.columna)

            if (valor_derecha.tipo.get_tipo() != TipoEnum.BOOLEAN):
                raise ValueError(
                    "Para realizar una operacion logica se necesita de un valor booleano al lado derecho ,Linea: "+self.linea+" ,Columna: "+self.columna)

        result = None

        if (self.tip == OpcionLogica.AND):
            result = valor_izquierdo and valor_derecha
            return Retorno(result, Tipo(TipoEnum.BOOLEAN, None))
        elif (self.tip == OpcionLogica.OR):
            result = valor_izquierdo or valor_derecha
            return Retorno(result, Tipo(TipoEnum.BOOLEAN, None))
        elif (self.tip == OpcionLogica.NOT):
            result = not valor_derecha
            return Retorno(result, Tipo(TipoEnum.BOOLEAN, None))

        return Retorno(None, Tipo(TipoEnum.ERROR, None))

    def graficar(self, scope, graphviz, padre):
        num = graphviz.declaraciones.length + 1
        node = "nodo" + num + \
            '[label="' + self.valOperacion[self.tipo] + '",shape="circle"];'
        graphviz.declaraciones.push(node)
        if (padre.length != 0):
            relacion = padre + ' -> ' + "nodo" + num
            graphviz.relaciones.push(relacion)

        self.izquierda.graficar(scope, graphviz, ("nodo" + num))
        self.derecha.graficar(scope, graphviz, ("nodo" + num))

##### CLASE OBTENER FUNCION ######


class ObtenerValFuncion(Exprecion):

    def __init__(self, linea, columna, identificador, parametros):
        super().__init__(linea, columna)
        self.identificador = identificador
        self.parametros = parametros

    def ejecutar(self, scope: Scope) -> Retorno:
        return Retorno(None, Tipo(TipoEnum.ERROR, None))

    def graficar(self, scope, graphviz, padre):
        print(scope, graphviz, padre)
        return None


class Operacion(Exprecion):

    def __init__(self, linea, columna, izquierda: Exprecion, derecha: Exprecion, tipo: OpcionOperacion):
        super().__init__(linea, columna)
        self.TipoOperacion = ['+', '-', '*', '/', '%', '^']
        self.izquierda = izquierda
        self.derecha = derecha
        self.tipo = tipo

    def ejecutar(self, scope: Scope) -> Retorno:
        result = None
        val_izquierdo = self.izquierda.ejecutar(scope)
        val_derecho = self.derecha.ejecutar(scope)
        if (val_derecho.value == None or val_izquierdo.value == None):
            if (val_izquierdo.value == None):
                raise ValueError("No se puede operar con un valor nulo Linea: " + self.linea + " ,Columna: " +
                                 self.columna + " ->  null " + self.TipoOperacion[self.tipo] + " " + val_derecho.value)
            else:
                raise ValueError("No se puede operar con un valor nulo Linea: " + self.linea + " ,Columna: " +
                                 self.columna + " ->  " + val_derecho.value + " " + self.TipoOperacion[self.tipo] + " null")

        # Debemos de verificar operacion entre tipos

        if (self.tipo == OpcionOperacion.SUMA):
            result = None
        elif (self.tipo == OpcionOperacion.RESTA):
            result = None
        elif (self.tipo == OpcionOperacion.MUL):
            result = None
        elif (self.tipo == OpcionOperacion.DIV):
            result = None
        elif (self.tipo == OpcionOperacion.MOD):
            result = None
        elif (self.tipo == OpcionOperacion.POT):
            result = None
        else:
            result = None

        return result

    def graficar(self, scope, graphviz, padre):
        num = graphviz.declaraciones.length + 1
        node = "nodo" + num + \
            ' [label="' + self.TipoOperacion[self.tipo] + '",shape="circle"];'
        graphviz.declaraciones.push(node)
        if (padre.length != 0):
            relacion = padre + ' -> ' + "nodo" + num
            graphviz.relaciones.push(relacion)

        self.izquierda.graficar(scope, graphviz, ("nodo" + num))
        self.derecha.graficar(scope, graphviz, ("nodo" + num))


class Relacional(Exprecion):
    def __init__(self, linea, columna, izquierda: Exprecion, derecha: Exprecion, tipo: OpcionRelacional):
        super().__init__(linea, columna)
        self.TipoRelacional = ['==', '!=', '<', '>', '<=', '>=']
        self.izquierda = izquierda
        self.derecha = derecha
        self.tipo = tipo

    def ejecutar(self, scope: Scope) -> Retorno:
        valor_izquierda = self.izquierda.ejecutar(scope)
        valor_derecha = self.derecha.ejecutar(scope)

        if (valor_izquierda.tipo.get_tipo() == Tipo.ERROR or valor_derecha.tipo.get_tipo() == Tipo.ERROR):
            raise ValueError("Errores previos antes de ralizar la comparacion , Linea: " +
                             self.linea + " ,Columna: " + self.columna)

        # Debemos de realizar la verificacion de los tipos de valores a comparar

        result = None

        if (self.tipo == OpcionRelacional.IGUAL):
            result = valor_izquierda == valor_derecha
            return Retorno(result, Tipo(TipoEnum.BOOLEAN))
        elif (self.tipo == OpcionRelacional.DIFERENTE):
            result = valor_izquierda != valor_derecha
            return Retorno(result, Tipo(TipoEnum.BOOLEAN))
        elif (self.tipo == OpcionRelacional.MENOR):
            result = valor_izquierda < valor_derecha
            return Retorno(result, Tipo(TipoEnum.BOOLEAN))
        elif (self.tipo == OpcionRelacional.MAYOR):
            result = valor_izquierda > valor_derecha
            return Retorno(result, Tipo(TipoEnum.BOOLEAN))
        elif (self.tipo == OpcionRelacional.MENOR_IGUAL):
            result = valor_izquierda <= valor_derecha
            return Retorno(result, Tipo(TipoEnum.BOOLEAN))
        elif (self.tipo == OpcionRelacional.MAYOR_IGUAL):
            result = valor_izquierda >= valor_derecha
            return Retorno(result, Tipo(TipoEnum.BOOLEAN))

        return Retorno(None, Tipo(TipoEnum.ERROR))

    def graficar(self, scope, graphviz, padre):
        num = graphviz.declaraciones.length + 1
        node = "nodo" + num + \
            ' [label="' + self.TipoRelacional[self.tipo] + '",shape="circle"];'
        graphviz.declaraciones.push(node)
        if (padre.length != 0):
            relacion = padre + ' -> ' + "nodo" + num
            graphviz.relaciones.push(relacion)

        self.izquierda.graficar(scope, graphviz, ("nodo" + num))
        self.derecha.graficar(scope, graphviz, ("nodo" + num))


class Asignacion(Instruccion):
    def __init__(self, linea, columna, identificador: str, valor: Exprecion):
        super().__init__(linea, columna)
        self.id = identificador
        self.valor = valor

    def ejecutar(self, scope: Scope) -> any:
        result = self.valor.ejecutar(scope)
        scope.modificar_variable(self.id, result.value, result.tipo)


class CallFuncion(Instruccion):
    def __init__(self, linea, columna, identificador: str, parametros: any):
        super().__init__(linea, columna)
        self.id = identificador
        self.parametros = parametros

    def ejecutar(self, scope: Scope) -> any:
        fun = scope.obtener_funcion(self.id)
        if (function != None):
            fun.ejecutar(scope)


class Continuar(Instruccion):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)

    def ejecutar(self, scope: Scope) -> any:
        return None


class Declaracion(Instruccion):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)

    def ejecutar(self, scope: Scope) -> any:
        result = self.valor.ejecutar(scope)
        scope.declarar_variable(self.id, result.value, result.tipo)


class Detener(Instruccion):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)

    def ejecutar(self, scope: Scope) -> any:
        return None


class Sentencias(Instruccion):
    def __init__(self, linea, columna, intrucciones: list):
        super().__init__(linea, columna)
        self.intrucciones = Instruccion

    def ejecutar(self, scope: Scope) -> Retorno:

        for instr in self.intrucciones:
            if isinstance(instr, Instruccion):
                if isinstance(instr, Detener):
                    return instr
                elif isinstance(instr, Continuar):
                    return instr
                elif isinstance(instr, Retornar):
                    elemento = instr.ejecutar(scope)
                    return Retornar(Literal(elemento.value, instr.linea, instr.columna, elemento.tipo), instr.linea, instr.columna)
                else:
                    elemento = instr.ejecutar(scope)
                    if isinstance(elemento, Detener):
                        return elemento
                    elif isinstance(elemento, Continuar):
                        return elemento
                    elif isinstance(elemento, Retornar):
                        ele = elemento.ejecutar(scope)
                        return Retornar(Literal(ele.value, instr.linea, instr.columna, ele.tipo), instr.linea, instr.columna)

    def graficar(self, scope, graphviz, sub_name_node, padre):
        # iteramos en cada una de las instrucciones de la lista y ejecutamos su metodo graficar
        for intructions in self.intrucciones:
            intructions.graficar(scope, graphviz, sub_name_node, padre)


class Funcion(Instruccion):

    def __init__(self, linea, columna, identificador: str, tipo: Tipo, sentancias: Sentencias | None):
        super().__init__(linea, columna)
        self.id = identificador
        self.tipo = tipo
        self.sentencias = sentancias

    def ejecutar(self, scope: Scope) -> Retorno:
        result = self.sentencias.ejecutar(scope)
        return result

    def graficar(self, scope, graphviz, padre) -> None:
        print("Graficacion de una funcion")


class Mientras(Instruccion):
    def __init__(self, linea, columna, condicion: Exprecion, sentencias: Sentencias | None):
        super().__init__(linea, columna)
        self.condicion = condicion
        self.sentencias = sentencias

    def ejecutar(self, scope: Scope) -> any:
        condicion = self.condicion.ejecutar(scope)

        # Debemos de verificar el boolean de un any
        if (condicion.tipo.get_tipo() != TipoEnum.BOOLEAN):
            raise ValueError(
                "La condicion de Mientras no es de tipo Boolean Linea: "+self.linea+" ,Columna: "+self.columna)

        while (condicion.value):
            result = self.sentencias.ejecutar(scope)
            if (isinstance(result, Detener)):
                break
            elif (isinstance(result, Continuar)):
                continue
            elif (isinstance(result, Retornar)):
                return result

            condicion = self.condicion.ejecutar(scope)
            # Debemos de verificar el boolean de un any
            if (condicion.tipo.get_tipo() != TipoEnum.BOOLEAN):
                raise ValueError(
                    "La condicion de Mientras no es de tipo Boolean Linea: "+self.linea+" ,Columna: "+self.columna)


class OpcionPara(Enum):
    SUM_PARA = 0
    RES_PARA = 1


class Para(Instruccion):
    def __init__(self, linea, columna, opPara: int, valVar: Exprecion, varIterator: str, sentencias: Sentencias, expr: Exprecion):
        super().__init__(linea, columna)
        self.opPara = opPara
        self.valVar = valVar
        self.varIterator = varIterator
        self.sentencias = sentencias
        self.expr = expr

    def ejecutar(self, scope: Scope) -> any:
        newScope = Scope
        paso = 0
        if (self.opPara == OpcionPara.SUM_PARA):
            paso = 1
        else:
            paso = -1

        exp1 = Acceder(self.varIterator, self.linea, self.columna)
        exp2 = Literal(paso, self.linea, self.columna, Tipo.INT)

        value = self.valVar.ejecutar(newScope)
        newScope.declararVariable(
            self.varIterator, value.value, Tipo.INT, self.linea, self.columna)

        newVal = Operacion(exp1, exp2, OpcionOperacion.SUMA,
                           self.linea, self.columna)
        asignar = Asignacion(self.varIterator, newVal,
                             self.linea, self.columna)

        condicion = self.expr.ejecutar(newScope)

        if (condicion.tipo != Tipo.BOOLEAN):
            raise ValueError(
                "La condicion de Para no es Boolean Linea: "+self.linea+" ,Columna: "+self.columna)

        while (condicion.value):
            result = self.sentencias.ejecutarPara(newScope)
            if (isinstance(Detener, result)):
                break
            elif (isinstance(Continuar, result)):
                asignar.ejecutar(newScope)
                condicion = self.expr.ejecutar(newScope)
                continue
            elif (isinstance(Retornar, result)):
                return result

            asignar.ejecutar(newScope)
            condicion = self.expr.ejecutar(newScope)
            if (condicion.tipo != Tipo.BOOLEAN):
                raise ValueError(
                    "La condicion de Para no es Boolean Linea: "+self.linea+" ,Columna: "+self.columna)

    def graficar(self, scope, graphviz, sub_name_node, padre):
        nume = graphviz.declaraciones.length + 1
        node = "nodo_" + sub_name_node + "_" + nume
        decl = node + '[label = "<n>Para"];'
        graphviz.declaraciones.push(decl)
        graphviz.relaciones.push((padre + ':n -> ' + node + ':n'))
        self.sentencias.graficar(scope, graphviz, sub_name_node, node)


class PrintPy(Instruccion):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)

    def ejecutar(self, scope: Scope) -> any:
        print(scope)
        return None


class Retornar(Instruccion):
    def __init__(self, linea, columna, exprecion: Exprecion):
        super().__init__(linea, columna)
        self.exprecion = exprecion

    def ejecutar(self, scope: Scope) -> any:
        valor = self.exprecion.ejecutar(scope)
        return valor

    def graficar(scope, graphviz, sub_name_node, padre):
        nume = graphviz.declaraciones.length + 1
        node = "nodo_" + sub_name_node + "_" + nume
        decl = node + '[label = "<n>Retorno"];'
        graphviz.declaraciones.push(decl)
        graphviz.relaciones.push((padre + ':n -> ' + node + ':n'))
        nume2 = graphviz.declaraciones.length + 1
        node2 = "nodo_" + sub_name_node + "_" + nume2
        decl2 = node2 + '[label = "<n>Exprecion"];'
        graphviz.declaraciones.push(decl2)
        graphviz.relaciones.push((node + ':n -> ' + node2 + ':n'))


class Si(Instruccion):
    def __init__(self, linea, columna, code_true, code_false):
        super().__init__(linea, columna)
        self.code_true = code_true
        self.code_false = code_false

    def ejecutar(self, scope: Scope) -> any:
        condicion = scope.obtenerVariable(self.identificador)
        if (condicion.tipo != TipoEnum.BOOLEAN):
            raise ValueError("La condicion de Si no es booleana Linea: " +
                             self.linea + " ,Columna: " + self.columna)
        if (condicion.value):
            return self.code_true.ejecutar(scope)
        else:
            return self.code_false.ejecutar(scope)

    def graficar(self, scope, graphviz, padre):
        nume = graphviz.declaraciones.length + 1
        node_si = "nodo_" + self.sub_name_node + "_" + nume
        decl = node_si + '[label = "<n>Si"];'
        graphviz.declaraciones.push(decl)
        graphviz.relaciones.push((padre + ':n -> ' + node_si + ':n'))
        self.code_true.graficar(scope, graphviz, self.sub_name_node, node_si)
        if (self.code_false != None):
            nume = graphviz.declaraciones.length + 1
            node_sino = "nodo_" + self.sub_name_node + "_" + nume
            decl = node_sino + '[label = "<n>Sino"];'
            graphviz.declaraciones.push(decl)
            graphviz.relaciones.push((node_si + ':n -> ' + node_sino + ':n'))
            self.code_false.graficar(
                scope, graphviz, self.code_true, self.sub_name_node, node_sino)


class Funciones:
    def __init__(self):
        self.diccionario = {}

    def add(self, clave: str, valor: Funcion):
        if clave in self.diccionario:
            raise ValueError(
                f"La variable \"{str(clave)}\" ya esta definida en este scope")
        else:
            self.diccionario[clave] = valor

    def has(self, clave: str) -> bool:
        return (clave in self.diccionario)

    def get(self, clave: str) -> Funcion:
        if clave in self.diccionario:
            return self.diccionario[clave]
        else:
            return None

    def delete(self, clave: str) -> None:
        if clave in self.diccionario:
            del self.diccionario["clave"]

    def get_diccionario(self):
        return self.diccionario


class Variables:
    def __init__(self):
        self.diccionario = {}

    def add(self, clave: str, valor: Simbolo):
        if clave in self.diccionario:
            raise ValueError(
                f"La funcion \"{str(clave)}\" ya esta definida en este scope")
        else:
            self.diccionario[clave] = valor

    def update(self, clave: str, valor: any, tipo: Tipo):
        if clave in self.diccionario:
            val = self.diccionario[clave]
            val.valor = valor
            val.tipo = tipo
            self.diccionario[clave] = val
        else:
            raise ValueError(
                f"La funcion \"{str(clave)}\" ya esta definida en este scope")

    def has(self, clave: str):
        return (clave in self.diccionario)

    def get(self, clave: str):
        if clave in self.diccionario:
            return self.diccionario[clave]
        else:
            return None

    def delete(self, clave: str):
        if clave in self.diccionario:
            del self.diccionario["clave"]

    def get_diccionario(self):
        return self.diccionario
