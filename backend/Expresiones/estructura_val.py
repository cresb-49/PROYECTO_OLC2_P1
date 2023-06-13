from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum


class EstructuraVal(Abstract):
    def __init__(self, resultado, linea, columna, tipo_secundario, contenido):
        super().__init__(resultado, linea, columna)
        self.tipo = TipoEnum.STRUCT
        self.tipo_secundario = tipo_secundario
        self.contenido = contenido

    def __str__(self):
        return f"EstructuraVal: tipo={self.tipo}, tipo_secundario={self.tipo_secundario}, contenido={self.contenido}"

    def ejecutar(self, scope):
        diccionario_values = dict()
        try:
            for clave in self.contenido:
                resultado = self.contenido[clave].ejecutar(scope)
                diccionario_values[clave] = resultado
            # Validacion de tipos asignados al struct
            estructura_base = scope.obtener_estructura(self.tipo_secundario)
            diccionario_base = estructura_base.composicion
            for clave in diccionario_values:
                val_asignar = diccionario_values[clave]
                val_correspondiente = diccionario_base[clave]
                # print(val_asignar['tipo'])
                # print(val_correspondiente['tipo'])
                if (not (val_correspondiente['tipo'] == val_asignar['tipo'] or val_correspondiente['tipo'] == TipoEnum.ANY)):
                    concat = f'Error al asignar valor al struct el parametro es de tipo: {val_correspondiente["tipo"].value} y recibio un parametro de tipo: {val_asignar["tipo"]}'
                    self.resultado.add_error(
                        'Semantico', concat, self.linea, self.columna)
                    val_asignar = {"value": None, "tipo": TipoEnum.ERROR,
                                   "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
                diccionario_values[clave] = val_asignar
            # Termino de la verificacion ahora debemos de retornar el valor del strut para ser declarado\
            return {"value": diccionario_values, "tipo": self.tipo, "tipo_secundario": self.tipo_secundario, "linea": self.linea, "columna": self.columna}
        except Exception as e:
            concat = f'Error de estructura: {str(e)}'
            self.resultado.add_error('Semantico', concat, self.linea, self.columna)
            return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        pass
