from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum


class Funcion(Abstract):

    def __init__(self, resultado, linea, columna, id, tipo, tipo_secundario, parametros, sentancias):
        super().__init__(resultado, linea, columna)
        self.id = id
        self.tipo = tipo
        self.sentencias = sentancias
        self.parametros = parametros
        self.tipo_secundario = tipo_secundario

    def __str__(self):
        return f"Funcion: {self.id}, tipo: {self.tipo}, tipo_secundario: {self.tipo_secundario}, parametros: {self.parametros}"

    def ejecutar(self, scope):
        if self.sentencias != None:
            result = self.sentencias.ejecutar(scope)
            if self.validacion_salida_funccion(result):
                val = {"value": result['value'], "tipo": result['tipo'],
                       "tipo_secundario": result['tipo_secundario'], "linea": self.linea, "columna": self.columna}
                print(f'Funcion -> {self.id} retorna -> ', val)
                return val
                # print('aquies es')
                # return {"value": result['value'], "tipo": result['tipo'], "tipo_secundario": result['tipo_tiposecundario'], "linea": self.linea, "columna": self.columna}
            else:
                val = {"value": None, "tipo": self.tipo, "tipo_secundario": self.tipo_secundario,
                       "linea": self.linea, "columna": self.columna}
                print(f'Funcion -> {self.id} retorna -> ', val)
                return val
                # if result != None:
                #     # Validar el tipo de retorno de la funcion
                #     return {"value": None, "tipo": self.tipo, "tipo_secundario": self.tipo_secundario, "linea": self.linea, "columna": self.columna}
                # else:
                #     if self.tipo == TipoEnum.ARRAY or self.tipo == TipoEnum.BOOLEAN or self.tipo == TipoEnum.NUMBER or self.tipo == TipoEnum.STRING or self.tipo == TipoEnum.STRUCT:
                #         self.resultado.add_error(
                #             'Semantico', f'La funcion "{self.id}" necesita retornar un valor de tipo {self.tipo.value} agregue la instruccion', self.linea, self.columna)
                #         return {"value": 'Null', "tipo": TipoEnum.NULL, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
                #     else:
                #         return {"value": None, "tipo": TipoEnum.ANY, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        else:
            val = {"value": None, "tipo": self.tipo, "tipo_secundario": self.tipo_secundario,
                   "linea": self.linea, "columna": self.columna}
            print(f'Funcion -> {self.id} retorna -> ', val)
            return val
            # return {"value": '', "tipo": TipoEnum.ANY, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def validacion_salida_funccion(self, result: dict) -> bool:
        if result == None:
            return False
        tipo: TipoEnum = result['tipo']
        if (self.tipo == tipo):
            tipo_secundario = result['tipo_secundario']
            if self.tipo == TipoEnum.ARRAY or self.tipo == TipoEnum.STRUCT:
                if tipo_secundario == self.tipo_secundario:
                    return True
                else:
                    self.resultado.add_error(
                        'Semantico', f'La funcion "{self.id}" de tipo {self.tipo.value} necesita retornar un sub tipo : {self.tipo_secundario}', self.linea, self.columna)
                    print(
                        'Semantico', f'La funcion "{self.id}" de tipo {self.tipo.value} necesita retornar un sub tipo : {self.tipo_secundario}', self.linea, self.columna)
                    return False
            else:
                return True
        elif self.tipo == TipoEnum.ANY:
            return True
        else:
            self.resultado.add_error(
                'Semantico', f'La funcion "{self.id}" necesita retornar un valor de tipo {self.tipo.value} y esta retornando un valor de tipo {tipo.value}', self.linea, self.columna)
            print(
                'Semantico', f'La funcion "{self.id}" necesita retornar un valor de tipo {self.tipo.value} y esta retornando un valor de tipo {tipo.value}', self.linea, self.columna)
            return False

    def graficar(self, graphviz, padre):
        mode_funcion = graphviz.add_nodo('Funcion:'+self.id, padre)
        node_parametros = graphviz.add_nodo('parametros', mode_funcion)
        if self.parametros!=None:
            for param in self.parametros:
                param.graficar(graphviz,node_parametros)
        if (self.sentencias != None):
            self.sentencias.graficar(graphviz, mode_funcion)

    def generar_c3d(self,scope):
        pass