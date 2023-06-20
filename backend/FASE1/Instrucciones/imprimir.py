from FASE1.Abstract.abstract import Abstract
from FASE1.Symbol.tipoEnum import TipoEnum


from FASE1.Symbol.generador import Generador
from FASE1.Abstract.return__ import Return


class Imprimir(Abstract):
    def __init__(self, resultado, linea, columna, exprecion):
        super().__init__(resultado, linea, columna)
        self.exprecion = exprecion
        # CODIGO DE AYUDA REFERENCIA PARA LA EJECUCION
        self.resultado_valor = []  # Esto de aca es un array
        self.last_scope = None      # Referencia del ultimo scope generado

    def __str__(self):
        return f"Print -> Expresión: {self.exprecion}"

    def ejecutar(self, scope):
        self.last_scope = scope
        concat = ""
        for diccionario in self.exprecion:
            resultado = diccionario.ejecutar(scope)
            self.resultado_valor.append(resultado)
            if (isinstance(resultado, dict)):
                # si el tipo de dato es un array entonces debemos imprimirlo como tal
                if (resultado['tipo'] == TipoEnum.ARRAY):
                    concat = self.imprimir_array(resultado)
                elif (resultado['tipo'] == TipoEnum.STRUCT):
                    concat = self.imprimir_struct(resultado)
                # si no es un array solo imprimimos normal y mandamos ha guardar la imprecion en la consola
                else:
                    print_val = resultado['value'] if resultado['value'] != None else 'Null'
                    concat = concat + " " + str(print_val)
                    concat = concat[1:] if concat.startswith(" ") else concat
            else:
                print('Debuj imprimir -> ', resultado)
                self.resultado.add_error(
                    'Semantico', 'Hubo un error previo ha imprimir el valor.', self.linea, self.columna)
        self.resultado.consola.append(concat)
        print(concat)

    def imprimir_array(self, resultado):
        # mandamos ha guardar el string en la consola
        # return self.imprimir_array_recu(resultado).replace('\'', '').replace('\\', '').replace('\"', '')
        return self.imprimir_array_recu(resultado).replace('\'', '').replace('\\', '')

    def imprimir_struct(self, resultado):
        # concat es la variable que alojara todos los string del struct
        concat = "{"
        # por cada uno de los elementos principales en el value (titulos de propiedades del struct)
        for parametro in resultado['value']:
            # adjuntar al concat el titulo del parametro "parametro" y el value del parametro
            if resultado['value'][parametro]['tipo'] == TipoEnum.ARRAY:
                concat = concat + ' ' + \
                    str(parametro) + ': ' + \
                    str(self.imprimir_array(
                        resultado['value'][parametro])) + ','
            if resultado['value'][parametro]['tipo'] == TipoEnum.STRING:
                concat = concat + ' ' + \
                    str(parametro) + ': \"' + \
                    str(resultado['value'][parametro]['value'])+'\",'
            else:
                concat = concat + ' ' + \
                    str(parametro) + ': ' + \
                    str(resultado['value'][parametro]['value'])+','
        concat = concat[:-1]
        return concat + " }"

    # crea un string de array imprimible, si un elemento del array es un array entonces se convierte en funcion recursiva

    def imprimir_array_recu(self, resultado):
        contenido = []
        concat = ""
        # por cada uno de los stings contenidos en el aray de resultado ajuntamos el value del strin al array
        for string in resultado['value']:
            if (string['tipo'] == TipoEnum.ARRAY):
                concat = self.imprimir_array_recu(string)
            elif (string['tipo'] == TipoEnum.STRUCT):
                concat = self.imprimir_struct(string)
            elif (string['tipo'] == TipoEnum.STRING):
                concat = "\""+string['value']+"\""
            else:
                concat = string['value']
            contenido.append(concat)
        return str(contenido)

    def graficar(self, graphviz, padre):
        main = graphviz.add_nodo('print', padre)
        node_params = graphviz.add_nodo('params', main)
        for param in self.exprecion:
            param.graficar(graphviz, node_params)
        # self.exprecion.graficar(graphviz, padre)
        # graphviz.add_nodo(');', padre)

    def generar_c3d(self, scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()

        # TODO: por el momento solo el print del primer parametro

        for expr in self.exprecion:
            result = expr.generar_c3d(scope)
            # if len(self.exprecion) >= 2:
            #     generador.add_print_espacio()
            if isinstance(result, Return):
                if result.get_tipo() == TipoEnum.NUMBER:
                    self.imprimir_number(generador, result.get_value())
                elif result.get_tipo() == TipoEnum.BOOLEAN:
                    self.imprmir_bool(generador, result.get_value())
                elif result.get_tipo() == TipoEnum.STRING:
                    self.imprimir_string(generador, result.get_value())
                elif result.get_tipo() == TipoEnum.ANY:
                    self.imprimir_opciones_any(generador,result.get_tipo_aux(),result)
                else:
                    print("\033[31m"+'Encontre variable sin clasificar ->', result)
        generador.add_print_salto_linea()

    def imprmir_bool(self, generador, value):
        generador.add_print_number('f', value)

    def imprimir_string(self, generador, value):
        # Generamos la funcion nativa para imprimir cadenas
        generador.f_print_string()
        param_temp = generador.add_temp()
        # Recuperamos el tamanio actual del stack
        size = self.last_scope.get_size()
        # Agregamos vairbales temporales para recibir el valor del strign guardado con anterioridad
        generador.add_exp(param_temp, 'P', size, '+')
        generador.add_exp(param_temp, param_temp, '1', '+')
        generador.set_stack(param_temp, value)
        # Generacion de un nuevo entorno para el llamado de la funcion
        generador.new_env(size)
        generador.call_fun('printString')

        temp = generador.add_temp()
        generador.get_stack(temp, 'P')
        generador.ret_env(size)

    def imprimir_number(self, generador, result):
        generador.add_print_number('f', result)

    def imprimir_opciones_any(self,generador,tipo_aux,result):
        if tipo_aux == TipoEnum.NUMBER:
            self.imprimir_number(generador, result.get_value())
        elif tipo_aux == TipoEnum.BOOLEAN:
            self.imprmir_bool(generador, result.get_value())
        elif tipo_aux == TipoEnum.STRING:
            self.imprimir_string(generador, result.get_value())
        elif tipo_aux == TipoEnum.ANY:
            print("\033[31m"+'Encontre variable any dentro de any? ->', result)
        else:
            print("\033[31m"+'Encontre variable sin clasificar ->', result)