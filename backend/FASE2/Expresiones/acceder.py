from FASE2.Abstract.abstract import Abstract
from FASE2.Abstract.return__ import Return
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Symbol.generador import Generador
from FASE2.Symbol.Exception import Excepcion


class Acceder(Abstract):
    def __init__(self, resultado, linea, columna, id):
        super().__init__(resultado, linea, columna)
        self.tipo = TipoEnum.ANY
        self.id = id
        # CODIGO DE AYUDA REFERENCIA PARA LA EJECUCION
        self.resultado_valor = None
        self.last_scope = None

    def __str__(self):
        return f"Acceder -> Tipo: {self.tipo} Id: {self.id}"

    def ejecutar(self, scope):
        recuperacion = scope.obtener_variable(self.id)
        self.resultado_valor = recuperacion
        self.last_scope = scope
        if (recuperacion == None):
            self.resultado.add_error(
                'Semantico', f"La variable {self.id} no existe", self.linea, self.columna)
        else:
            if (recuperacion.tipo == TipoEnum.ANY):
                if recuperacion.tipo_secundario == TipoEnum.NUMBER.value:
                    return {"value": recuperacion.valor, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
                elif recuperacion.tipo_secundario == TipoEnum.BOOLEAN.value:
                    return {"value": recuperacion.valor, "tipo": TipoEnum.BOOLEAN, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
                elif recuperacion.tipo_secundario == TipoEnum.STRING.value:
                    return {"value": recuperacion.valor, "tipo": TipoEnum.STRING, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
                elif recuperacion.tipo_secundario == TipoEnum.STRUCT.value:
                    # Se debe realizar el calculo del tipo para el regreso
                    scope_global = self.resultado.get_scope_global()
                    tipo_secundario = self.validacion_struct(
                        scope_global, recuperacion.valor)
                    return {"value": recuperacion.valor, "tipo": TipoEnum.STRUCT, "tipo_secundario": tipo_secundario, "linea": self.linea, "columna": self.columna}
                elif recuperacion.tipo_secundario == TipoEnum.ARRAY.value:
                    # Se debe realizar el calculo de tipo para el regreso
                    if len(recuperacion.valor) != 0:
                        base = recuperacion.valor[0]['tipo']
                        if all(base == exp['tipo'] for exp in recuperacion.valor):
                            tipo_secundario = base.value
                            return {"value": recuperacion.valor, "tipo": TipoEnum.ARRAY, "tipo_secundario": tipo_secundario, "linea": self.linea, "columna": self.columna}
                        else:
                            return {"value": recuperacion.valor, "tipo": TipoEnum.ARRAY, "tipo_secundario": TipoEnum.ANY.value, "linea": self.linea, "columna": self.columna}
                    else:
                        return {"value": [], "tipo": TipoEnum.ARRAY, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
                elif recuperacion.tipo_secundario == TipoEnum.ANY.value:
                    return {"value": recuperacion.valor, "tipo": TipoEnum.ANY, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
                print('No devolvio nada acceder')
            elif (recuperacion.tipo == TipoEnum.ARRAY):
                return {"value": recuperacion.valor, "tipo": TipoEnum.ARRAY, "tipo_secundario": recuperacion.tipo_secundario, "linea": self.linea, "columna": self.columna}
            else:
                return {"value": recuperacion.valor, "tipo": recuperacion.tipo, "tipo_secundario": recuperacion.tipo_secundario, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        graphviz.add_nodo(self.id, padre)

    def validacion_struct(self, scope_global_fin_analisis, valor_recuperado):
        scope_tmp = scope_global_fin_analisis.estructuras.get_diccionario()
        resultados = []
        for estrucura in scope_tmp:
            diccionario_tmp = ((scope_tmp[estrucura]).composicion)
            if self.comparar_diccionarios(diccionario_tmp, valor_recuperado):
                resultados.append(scope_tmp[estrucura])
            if len(resultados) == 0:
                self.resultado.add_error(
                    'Semantico', 'El tipo de estructura no esta definina el proyecto', self.linea, self.columna)
            elif len(resultados) == 1:
                tipo_secundario = resultados[0].id
                print(tipo_secundario)
                return resultados[0].id
            else:
                self.resultado.add_error(
                    'Semantico', 'Existe ambiguedad al deducir la estructura', self.linea, self.columna)

    def comparar_diccionarios(self, diccionario1, diccionario2):
        claves1 = diccionario1.keys()
        claves2 = diccionario2.keys()
        if len(claves1) != len(claves2):
            return False
        for clave in claves1:
            if clave not in claves2:
                return False
        return True

    def generar_c3d(self, scope):
        # inicializamos las variables que hacen la generacion de codigo 3 direcciones
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        generador.add_comment(
            f"** compilacion de acceso de variable {self.id} **")
        # Recuperamos variable desde el ultimo scope generado
        result = scope.obtener_variable(self.id)
        if(result == None):
            return Excepcion("Semantico", "No se puedo encontrar la variable", self.linea, self.columna)
        #result = scope.obtener_variable(self.id)
        # Generamos un contenedor temporal para la variable que vamos a recuperar
        temp = generador.add_temp()
        # Generamos un variable para recuperar las posicion en el stack de la variable
        # Eliminamos los primeros 3 caracteres de lo recuperado
        # temporal_pos = result.simbolo_c3d.pos[4:]
        # temp_pos = result.simbolo_c3d.pos[4:]
        temporal_pos = result.simbolo_c3d.pos
        temp_pos = result.simbolo_c3d.pos
        
        print('debuj acceder->',temporal_pos)
        print('debuj acceder->',temp_pos)
        # Verificamos si la variable es global
        if not result.simbolo_c3d.is_global:
            temp_pos = generador.add_temp()
            generador.add_exp(temp_pos, 'P', temporal_pos, '+')
        # Intruccion para obtener la referencia del stack
        generador.get_stack(temp, temp_pos)
        # Retornamos los datos temp -> el valor que tomo del stack
        # El tipo de valor retornado en la ejecucion del codigo
        # Si la variable es temporal
        print('Debuj acceder->', result)
        tipo_variable = result.tipo
        self.tipo = tipo_variable
        if tipo_variable != TipoEnum.ANY and tipo_variable != TipoEnum.STRUCT:
            if (tipo_variable == TipoEnum.BOOLEAN):
                generador.add_comment(
                    f"** fin compilacion de acceso de variable {self.id} **")
                return self.definicion_variable_bool(temp, generador)
            else:
                generador.add_comment(
                    f"** fin compilacion de acceso de variable {self.id} **")
                return Return(temp, tipo_variable, True, None)
        else:
            calculo = self.calculo_tipo_aux(result.tipo_secundario)
            if calculo == TipoEnum.BOOLEAN:
                generador.add_comment(
                    f"** fin compilacion de acceso de variable {self.id} **")
                return self.definicion_variable_bool(temp, generador)
            else:
                generador.add_comment(
                    f"** fin compilacion de acceso de variable {self.id} **")
                return Return(temp, tipo_variable, True, self.calculo_tipo_aux(result.tipo_secundario))

    def calculo_tipo_aux(self, tipo_secundario):
        if tipo_secundario == TipoEnum.BOOLEAN.value:
            return TipoEnum.BOOLEAN
        elif tipo_secundario == TipoEnum.NUMBER.value:
            return TipoEnum.NUMBER
        elif tipo_secundario == TipoEnum.STRING.value:
            return TipoEnum.STRING
        elif tipo_secundario == TipoEnum.STRUCT.value:
            return TipoEnum.NUMBER
        else:
            return tipo_secundario

    def definicion_variable_bool(self, temp, generador: Generador):
        true_label = generador.new_label()

        false_label = generador.new_label()

        generador.add_if(temp, '1', '==', true_label)
        generador.add_goto(false_label)

        generador.add_comment(
            f"** fin compilacion de acceso de variable {self.id} **")
        generador.add_space()
        retorno = Return(None, TipoEnum.BOOLEAN, True, None)
        retorno.add_true_lbl(true_label)
        retorno.add_false_lbl(false_label)

        return retorno
