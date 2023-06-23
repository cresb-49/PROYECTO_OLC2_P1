from FASE2.Abstract.abstract import Abstract
from FASE2.Abstract.return__ import Return
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Symbol.generador import Generador
from FASE2.Symbol.scope import Scope


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
                else:
                    if val_correspondiente['tipo'] == TipoEnum.ARRAY:
                        if val_correspondiente['tipo_secundario'] == val_asignar['tipo_secundario']:
                            diccionario_values[clave] = val_asignar
                        else:
                            concat = f'Error al asignar valor al struct el parametro "{clave}" es de tipo: {val_correspondiente["tipo_secundario"]} y recibio un parametro de tipo: {val_asignar["tipo_secundario"]}'
                            self.resultado.add_error(
                                'Semantico', concat, self.linea, self.columna)
                            val_asignar = {"value": None, "tipo": TipoEnum.ERROR,
                                           "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
                    else:
                        diccionario_values[clave] = val_asignar
            # Termino de la verificacion ahora debemos de retornar el valor del strut para ser declarado\
            return {"value": diccionario_values, "tipo": self.tipo, "tipo_secundario": self.tipo_secundario, "linea": self.linea, "columna": self.columna}
        except Exception as e:
            concat = f'Error de estructura: {str(e)}'
            self.resultado.add_error(
                'Semantico', concat, self.linea, self.columna)
            return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        # anadimos un nodo padre que indique que el nodo es un stuct
        node_padre = graphviz.add_nodo('struct', padre)
        # por cada uno de los elementos que conforman el contenido:
        for clave in self.contenido:
            # creamos un nodo padre que contrendra el titulo del elemento en cuetion
            node_padre_elemento = graphviz.add_nodo(clave, node_padre)
            # al nodo con eltitulo agregamos un nodo con el valor del titulo
            self.contenido[clave].graficar(graphviz, node_padre_elemento)

    def generar_c3d(self, scope: Scope):

        print('Estoy generando valor de estrutura')
        gen_aux = Generador()
        generador = gen_aux.get_instance()

        # Generamos el temporal para guardar la posicion del heap
        generador.add_comment('Compilacion del valor de un struct')
        puntero_principal = generador.add_temp()
        temp_contador = generador.add_temp()
        generador.add_asig(puntero_principal, 'H')
        generador.add_asig(temp_contador, 'H')
        # Debemos de reservar el cantidad de espacios asociadas al struct
        size_struct = len(self.contenido)
        generador.add_exp('H', 'H', str(size_struct), '+')
        # Ya generados los tamanos del scope asignamos los valores en el heap en base al
        # contador y luego sumamos de uno en uno
        # Recuperamos la base del struct original
        struct_orginal = scope.obtener_estructura(self.tipo_secundario)
        print('Tipo del struct', self.tipo_secundario)
        print('Struct original', struct_orginal.configuracion)
        print('Size del struct', size_struct)
        for param in struct_orginal.configuracion:
            value = self.contenido[param]
            resultado: Return = value.generar_c3d(scope)
            generador.set_heap(temp_contador, resultado.get_value())
            generador.add_exp(temp_contador, temp_contador, '1', '+')
        generador.add_comment('Fin del compilado del valor de un struct')
        result: Return = Return(
            puntero_principal, TipoEnum.STRUCT, True, self.tipo_secundario)
        return result
