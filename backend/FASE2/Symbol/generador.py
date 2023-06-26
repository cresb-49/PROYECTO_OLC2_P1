class Generador:
    generator = None

    def __init__(self) -> None:
        # Contadores
        self.count_temp = 0
        self.count_label = 0

        # Label salida de programa
        self.label_out = ''
        
        # Codigo
        self.codigo = ""
        self.funcs = ''
        self.natives = ''
        self.in_func = False
        self.in_natives = False
        self.to_stringg = False
        self.to_string_numberr = False
        self.to_string_stringg = False
        self.to_string_booleann = False
        self.type_of_stringg = False
        self.type_of_numberr = False
        self.type_of_booleann = False
        self.type_of_structt = False
        self.to_exponentiall = False
        # Lista de temporales
        self.temps = []

        # TODO: Agregar la lista de nativas
        # Lista de Naivas
        self.print_string = False
        self.to_fixed = False
        self.to_lowerr = False
        self.to_upperr = False
        self.summ_strings = False
        self.compare_string = False
        self.lengthh = False
        self.out_of_bouns = False
        # Lista de imports
        self.imports = []
        self.imports2 = ['fmt', 'math']

    def get_instance(self):
        if Generador.generator == None:
            Generador.generator = Generador()
        return Generador.generator

    def clean_all(self):
        # Contadores
        self.count_temp = 0
        # codigo
        self.codigo = ""
        # Lista de temporales
        self.temps = []
        # Lista de nativas
        self.print_string = False

        self.imports = []
        self.imports2 = ['fmt', 'math']
        Generador.generator = Generador()

    #############
    # IMPORTS
    ############

    def set_import(self, lib):
        if lib not in self.imports:
            self.imports.append(lib)
        # if lib in self.imports2:
        #     self.imports2.remove(lib)
        # else:
        #     return
        # self.code = f'import(\n\t"{lib}"\n)\n'

     #############
    # CODE
    #############

    def get_header(self):
        code = '/* ---- HEADER ----- */\npackage main;\n\n'
        # print('debuj imports -> ',self.imports)
        if len(self.imports) > 0:
            tmp_import = ''
            for temp in self.imports:
                tmp_import += f'\t"{temp}"\n'
            code += f'import(\n{tmp_import})\n'
        if len(self.temps) > 0:
            code += 'var '
            for temp in self.temps:
                code += temp + ','
            code = code[:-1]
            code += " float64;\n\n"
        code += "var P, H float64;\nvar stack[30101999] float64;\nvar heap[30101999] float64;\n\n"
        return code

    def get_code(self):
        if self.label_out != '':
            # self.put_label(self.label_out)
            pass
        return f'{self.get_header()}{self.natives}{self.funcs}\nfunc main(){{\n{self.codigo}\n}}'

    def code_in(self, code, tab="\t"):
        if self.in_natives:
            if self.natives == '':
                self.natives = self.natives + '/* --- NATIVAS --- */\n'
            self.natives = self.natives + tab + code
        elif self.in_func:
            if self.funcs == '':
                self.funcs = self.funcs + '/* --- FUNCION --- */\n'
            self.funcs = self.funcs + tab + code
        else:
            self.codigo = self.codigo + tab + code

    def add_comment(self, comment):
        self.code_in(f'/* {comment} */\n')

    def add_space(self):
        self.code_in('\n')

    #########################
    # Manejo de Temporales
    ########################

    def add_temp(self):
        temp = f't{self.count_temp}'
        self.count_temp += 1
        self.temps.append(temp)
        return temp  # t1 t2 t3 t4 t5

    #####################
    # Manejo de Labels
    #####################

    def new_label(self):
        label = f'L{self.count_label}'
        self.count_label += 1
        return label  # Agregamos un nuevo label L1 L2 L3 L4 L5

    def put_label(self, label):
        self.code_in(f'{label}:\n')  # Lo definimos en el codigo -> L1: L2: L3:

    def add_ident(self):
        self.code_in("")

    def add_space(self):
        self.code_in("\n")

    ###################
    # GOTO
    ###################

    def add_goto(self, label):
        self.code_in(f'goto {label};\n')
    
    def add_goto_out(self):
        self.code_in(f'goto {self.label_out};\n')

    ###################
    # IF
    ###################

    def add_if(self, left, right, op, label):
        self.code_in(f'if {left} {op} {right} {{goto {label};}}\n')

    ###################
    # EXPRESIONES
    ###################

    def add_exp(self, result, left, right, op):
        if op == '^':
            self.set_import('math')
            self.code_in(f'{result} =  math.Pow({left}, {right});\n')
        elif op == '%':
            self.code_in(
                f'{result} =  float64(int({left}) {op} int({right}));\n')
        else:
            self.code_in(f'{result} = {left} {op} {right};\n')

    def add_asig(self, result, left):
        self.code_in(f'{result} = {left};\n')

    ###############
    # FUNCS
    ###############

    def add_begin_func(self, id):
        if not self.in_natives:
            self.in_func = True
        self.code_in(f'func {id}(){{\n')

    def add_end_func(self):
        self.code_in('}\n')
        if not self.in_natives:
            self.in_func = False

    ###############
    # STACK
    ###############

    def set_stack(self, pos, value):
        self.code_in(f'stack[int({pos})] = {value};\n')

    def get_stack(self, place, pos):
        self.code_in(f'{place} = stack[int({pos})];\n')

     #############
    # ENTORNO
    #############

    def new_env(self, size):
        self.code_in('/* --- NUEVO ENTORNO --- */\n')
        self.code_in(f'P = P + {size};\n')

    def call_fun(self, id):
        self.code_in(f'{id}();\n')

    def ret_env(self, size):
        self.code_in(f'P = P - {size};\n')
        self.code_in('/* --- RETORNO DE ENTORNO --- */\n')

    ###############
    # HEAP
    ###############

    def set_heap(self, pos, value):
        self.code_in(f'heap[int({pos})] = {value};\n')

    def get_heap(self, place, pos):
        self.code_in(f'{place} = heap[int({pos})];\n')

    def next_heap(self):
        self.code_in('H = H + 1;\n')

    ###############
    # INSTRUCCIONES
    ###############
    def add_debuj(self, type, value):
        self.set_import('fmt')
        self.code_in(f'fmt.Printf("%{type}", {value});\n')  # %d %f %c %s

    def add_print(self, type, value):
        self.set_import('fmt')
        self.code_in(f'fmt.Printf("%{type}", int({value}));\n')  # %d %f %c %s

    def add_print_number(self, type, value):
        self.set_import('fmt')
        self.code_in(f'fmt.Printf("%{type}", {value});\n')  # %d %f %c %s

    def print_true(self):
        self.set_import('fmt')
        self.add_ident()
        self.add_print('c', 116)
        self.add_ident()
        self.add_print('c', 114)
        self.add_ident()
        self.add_print('c', 117)
        self.add_ident()
        self.add_print('c', 101)

    def print_false(self):
        self.set_import('fmt')
        self.add_ident()
        self.add_print('c', 102)
        self.add_ident()
        self.add_print('c', 97)
        self.add_ident()
        self.add_print('c', 108)
        self.add_ident()
        self.add_print('c', 115)
        self.add_ident()
        self.add_print('c', 101)

    def add_print_salto_linea(self):
        self.set_import('fmt')
        self.code_in('fmt.Println("")\n')

    def add_print_espacio(self):
        self.set_import('fmt')
        self.code_in('fmt.Print(" ")\n')
    ###############
    # NATIVAS
    ###############

    def f_print_string(self):
        self.set_import('fmt')
        if self.print_string:
            return
        self.print_string = True
        self.in_natives = True

        self.add_begin_func('printString')
        # Label para salir de la funcion
        return_lbl = self.new_label()
        # Label para la comparacion para buscar fin de cadena
        compare_lbl = self.new_label()
        # Temporal puntero a stack
        tempo_p = self.add_temp()
        # Temporal puntero Heap
        temp_h = self.add_temp()
        self.add_exp(tempo_p, 'P', '1', '+')
        self.get_stack(temp_h, tempo_p)
        # Temporal para comparar
        temp_c = self.add_temp()
        self.put_label(compare_lbl)
        self.add_ident()
        self.get_heap(temp_c, temp_h)
        self.add_ident()
        self.add_if(temp_c, '-1', '==', return_lbl)
        self.add_ident()
        self.add_print('c', temp_c)
        self.add_ident()
        self.add_exp(temp_h, temp_h, '1', '+')
        self.add_ident()
        self.add_goto(compare_lbl)
        self.put_label(return_lbl)
        self.add_end_func()
        self.in_natives = False

    def fcompare_string(self):
        if self.compare_string:
            return
        self.compare_string = True
        self.in_natives = True

        self.add_begin_func("compareString")
        # Label para salir de la funcion
        return_lbl = self.new_label()

        t2 = self.add_temp()
        self.add_exp(t2, 'P', '1', '+')
        t3 = self.add_temp()
        self.get_stack(t3, t2)
        self.add_exp(t2, t2, '1', '+')
        t4 = self.add_temp()
        self.get_stack(t4, t2)

        l1 = self.new_label()
        l2 = self.new_label()
        l3 = self.new_label()
        self.put_label(l1)

        t5 = self.add_temp()
        self.add_ident()
        self.get_heap(t5, t3)

        t6 = self.add_temp()
        self.add_ident()
        self.get_heap(t6, t4)

        self.add_ident()
        self.add_if(t5, t6, '!=', l3)
        self.add_ident()
        self.add_if(t5, '-1', '==', l2)

        self.add_ident()
        self.add_exp(t3, t3, '1', '+')
        self.add_ident()
        self.add_exp(t4, t4, '1', '+')
        self.add_ident()
        self.add_goto(l1)

        self.put_label(l2)
        self.add_ident()
        self.set_stack('P', '1')
        self.add_ident()
        self.add_goto(return_lbl)
        self.put_label(l3)
        self.add_ident()
        self.set_stack('P', '0')
        self.put_label(return_lbl)
        self.add_end_func()
        self.in_natives = False

    def too_fixed(self):
        if self.to_fixed:
            return
        self.to_fixed = True
        self.in_natives = True

        # agregamos la libreia math para poder hacer el round especifico
        self.set_import('math')
        self.set_import('strconv')
        self.add_begin_func("toFixed")

        t2 = self.add_temp()
        self.add_exp(t2, 'P', '1', '+')
        # variable temporal en donde se alojara el valor del numero base
        t3 = self.add_temp()
        self.get_stack(t3, t2)
        self.add_exp(t2, t2, '1', '+')

        # variable temporal que contendra el numero de presicion
        t4 = self.add_temp()
        self.get_stack(t4, t2)

        # Termporal que guardara el pow con exponente t4
        pow = self.add_temp()
        self.add_asig(pow, f"math.Pow(10, {t4})")

        # temporal que guardara la multiplicacion del t3 por el t5
        round_content = self.add_temp()
        self.add_exp(round_content, t3, pow, "*")

        # temporal que guarda el resultado de round
        round = self.add_temp()
        self.add_asig(round, f"math.Round({round_content})")

        # temporal que guarda el resultado de round dividido el pow
        respuesta = self.add_temp()
        self.add_exp(respuesta, round, pow, "/")

        # seteamos el pointer con el valor de la operacion to fixed
        self.set_stack(
            'P', respuesta)

        self.add_end_func()
        self.in_natives = False

    def to_lower(self):
        if (self.to_lowerr):
            return
        self.to_lowerr = True
        self.in_natives = True
        # creamos la funcion toUpperCase
        self.add_begin_func('toLowerCase')

        return_et = self.new_label()  # Se crea etiqueta para moverse fuera de la funcion

        # Se crea etiqueta de comparacion para detectar fin del string
        compare_et = self.new_label()

        temp_p = self.add_temp()  # Se crea temporal puntero a stack

        temp_h = self.add_temp()  # Se crea temporal puntero a heap

        # Se aumenta la posicion del stack en 1
        self.add_exp(temp_p, 'P', '1', '+')

        self.get_stack(temp_h, temp_p)  # Se mueve el valor del stack al heap

        temp_c = self.add_temp()  # Se crea temporal de comparacion

        self.put_label(compare_et)  # Se pone la etiqueta de comparacion

        self.get_heap(temp_c, temp_h)  # Se mueve el valor del heap al stack

        # Se crea goto condicional que comprueba si el temporal de comparacion tiene valor de -1
        self.add_if(temp_c, '-1', '==', return_et)

        temp = self.add_temp()  # Se agrega temporal

        pass_et = self.new_label()  # Se crea etiqueta de conversion

        # Goto condicional hacia la etiqueta de conversion para comprobar si valor es mayuscula
        self.add_if(temp_c, '65', '<', pass_et)

        # Goto condicional hacia etiqueta de conversion para comprobar si el valor no es minuscula
        self.add_if(temp_c, '90', '>', pass_et)

        # Se reduce en 32 el valor de temporal de comparacion y se guarda en temporal (se convierte en minuscula)
        self.add_exp(temp, temp_c, '32', '+')

        # Se guarda el valor de temporal en el heap
        self.set_heap(temp_h, temp)

        self.put_label(pass_et)  # Se pone la etiqueta de conversion

        # Se aumenta en 1 la posicion del heap
        self.add_exp(temp_h, temp_h, '1', '+')

        self.add_goto(compare_et)  # Se agrega goto a etiqueta condicional

        # Se pone la etiqueta de salida de la funcion
        self.put_label(return_et)

        self.add_end_func()  # Se agrega fin de funcion

        self.in_natives = False  # Se desactiva flag que indica que se esta en una funcion nativa

    def to_upper(self):
        if (self.to_upperr):
            return
        self.to_upperr = True
        self.in_natives = True
        # creamos la funcion toUpperCase
        self.add_begin_func('toUpperCase')

        return_et = self.new_label()  # Se crea etiqueta para moverse fuera de la funcion

        # Se crea etiqueta de comparacion para detectar fin del string
        compare_et = self.new_label()

        temp_p = self.add_temp()  # Se crea temporal puntero a stack

        temp_h = self.add_temp()  # Se crea temporal puntero a heap

        # Se aumenta la posicion del stack en 1
        self.add_exp(temp_p, 'P', '1', '+')

        self.get_stack(temp_h, temp_p)  # Se mueve el valor del stack al heap

        temp_c = self.add_temp()  # Se crea temporal de comparacion

        self.put_label(compare_et)  # Se pone la etiqueta de comparacion

        self.get_heap(temp_c, temp_h)  # Se mueve el valor del heap al stack

        # Se crea goto condicional que comprueba si el temporal de comparacion tiene valor de -1
        self.add_if(temp_c, '-1', '==', return_et)

        temp = self.add_temp()  # Se agrega temporal

        pass_et = self.new_label()  # Se crea etiqueta de conversion

        # Goto condicional hacia la etiqueta de conversion para comprobar si valor es mayuscula
        self.add_if(temp_c, '97', '<', pass_et)

        # Goto condicional hacia etiqueta de conversion para comprobar si el valor no es minuscula
        self.add_if(temp_c, '122', '>', pass_et)

        # Se reduce en 32 el valor de temporal de comparacion y se guarda en temporal (se convierte en minuscula)
        self.add_exp(temp, temp_c, '32', '-')

        # Se guarda el valor de temporal en el heap
        self.set_heap(temp_h, temp)

        self.put_label(pass_et)  # Se pone la etiqueta de conversion

        # Se aumenta en 1 la posicion del heap
        self.add_exp(temp_h, temp_h, '1', '+')

        self.add_goto(compare_et)  # Se agrega goto a etiqueta condicional

        # Se pone la etiqueta de salida de la funcion
        self.put_label(return_et)

        self.add_end_func()  # Se agrega fin de funcion

        self.in_natives = False  # Se desactiva flag que indica que se esta en una funcion nativa

    def sum_strings(self):
        # if que reconoce si ya ha sido agregada la funcion sumStrings
        if self.summ_strings:
            return
        self.summ_strings = True
        self.in_natives = True
        # declaramos la nueva funcion
        self.add_begin_func("sumStrings")
        # creamos una variable que guardara el inicio de la nueva cadena
        t0 = self.add_temp()
        self.add_asig(t0, 'H')

        # Label para salir de la funcion
        return_lbl = self.new_label()
        # creamos una nueva temporal
        t2 = self.add_temp()
        # a la temporal asignamos la posicion actual de P
        self.add_exp(t2, 'P', '1', '+')
        # anadir temporal que guardara la referencia del stack en t2 y contendra la primera cadena
        t3 = self.add_temp()
        self.get_stack(t3, t2)
        self.add_exp(t2, t2, '1', '+')

        # anadimos el temporal que conentra la segunda cadena
        t4 = self.add_temp()
        self.get_stack(t4, t2)

        # label de incializacion del primer ciclo
        l1 = self.new_label()
        # label  que inicia la agregacion de los caracteres de la primera cadena a la cadena nueva
        l3 = self.new_label()

        # label de iniciaizacion del segundo ciclo
        l2 = self.new_label()
        # label  que inicia la agregacion de los caracteres de la segunda cadena a la cadena nueva
        l4 = self.new_label()

        # iniciamos el primer ciclo
        self.put_label(l1)

        # obtenemos el caracter de la primera cadena contenido en el heap
        t5 = self.add_temp()
        self.add_ident()
        self.get_heap(t5, t3)

        self.add_ident()

        # si la cadena es diferente de menos 1 entonces agregamos hacemos salto a la etiqueta que guarda la primera cadena
        self.add_if(t5, '-1', '!=', l3)
        self.add_ident()
        self.add_if(t5, '-1', '==', l2)

        ########################################
        # AGREGACION CARACTERES PRIMERA CADENA #
        ########################################

        # anadimos el valor t5 a una nueva posicion en el heap y retornamos a la label del primer bucle
        self.put_label(l3)
        self.add_ident()
        self.set_heap('H', t5)
        self.add_ident()
        self.next_heap()
        self.add_ident()
        self.add_exp(t3, t3, '1', '+')
        self.add_ident()
        self.add_goto(l1)

        #################
        # SEGUNDO CICLO #
        #################

        # debemos iniciar el segundo ciclo que anade los caracters de la segunda cadena a la nueva cadena
        self.put_label(l2)
        # obtenemos el caracter de la primera cadena contenido en el heap
        t6 = self.add_temp()
        self.add_ident()
        self.get_heap(t6, t4)
        self.add_ident()
        # si la cadena es diferente de menos 1 entonces agregamos hacemos salto a la etiqueta que guarda la primera cadena
        self.add_if(t6, '-1', '!=', l4)
        self.add_ident()
        self.add_if(t6, '-1', '==', return_lbl)

        ########################################
        # AGREGACION CARACTERES SEGUNDA CADENA #
        ########################################

        # anadimos el valor t6 a una nueva posicion en el heap y retornamos a la label del primer bucle
        self.put_label(l4)
        self.add_ident()
        self.set_heap('H', t6)
        self.add_ident()
        self.next_heap()
        self.add_ident()
        self.add_exp(t4, t4, '1', '+')
        self.add_ident()
        self.add_goto(l2)

        self.put_label(return_lbl)

        self.add_ident()
        # anadimos el caracter -1 a la nueva cadena
        self.set_heap('H', '-1')
        self.add_ident()
        # aumentamos en uno el heap
        self.next_heap()
        self.add_ident()
        # devolvemos la posicion inicial de la cadena
        self.set_stack('P', t0)
        self.add_end_func()
        self.in_natives = False

    def length(self):
        # if que reconoce si ya ha sido agregada la funcion length
        if self.lengthh:
            return
        self.lengthh = True
        self.in_natives = True
        # declaramos la nueva funcion
        self.add_begin_func("length")

        # declaracion de una temporal contadora
        t0 = self.add_temp()
        self.add_asig(t0, '0')  # inicializamos la temporal en 0

        # creamos una nueva temporal
        t2 = self.add_temp()
        # a la temporal asignamos la posicion actual de P
        self.add_exp(t2, 'P', '1', '+')
        # anadir temporal que guardara la referencia del stack en t2 y contendra la primera cadena
        t3 = self.add_temp()
        self.get_stack(t3, t2)
        self.add_exp(t2, t2, '1', '+')

        #########################
        # DECLARACION DE LABELS #
        #########################

        # Label para salir de la funcion
        return_lbl = self.new_label()
        # Label para iniciar el ciclo
        l1 = self.new_label()
        # Label para la acumulacion del contador
        l2 = self.new_label()

        #######################
        # INICIO DEL CICLO    #
        #######################

        # marcamos la label que inicia el ciclo
        self.put_label(l1)
        # obtenemos el caracter de la primera cadena contenido en el heap
        t6 = self.add_temp()
        self.add_ident()
        self.get_heap(t6, t3)
        self.add_ident()
        # si la cadena es diferente de menos 1 entonces agregamos hacemos salto a la etiqueta que guarda la primera cadena
        self.add_if(t6, '-1', '!=', l2)
        self.add_ident()
        # Si se encontro el -1 entonces debemos terminar el metodo
        self.add_if(t6, '-1', '==', return_lbl)

        ###############################
        # Acumulacion del contador    #
        ###############################

        # marcamos la label que hace la acumulacion del contador
        self.put_label(l2)
        self.add_ident()
        # acumulamos 1 en la temporal contadora
        self.add_exp(t0, t0, '1', '+')
        self.add_ident()
        self.add_exp(t3, t3, '1', '+')
        self.add_ident()
        # regresamos a la label que abre el ciclo
        self.add_goto(l1)

        ####################################
        # Declaracion del final del metodo #
        ####################################

        # declaramos la label que termina el metodo
        self.put_label(return_lbl)
        # en el stack devolvemos el valor final de la variable contadora
        self.set_stack('P', t0)
        self.add_end_func()
        self.in_natives = False

    # def to_string_number(self):
    #     # if que reconoce si ya ha sido agregada la funcion to_string
    #     if self.to_string_numberr:
    #         return
    #     self.to_string_numberr = True
    #     self.in_natives = True

    #     # anadimos la libreria de manipulacion de string
    #     self.set_import('strconv')

    #     # declaramos la nueva funcion to_string_number
    #     self.add_begin_func("to_string_number")
    #     # creamos una nueva temporal
    #     t2 = self.add_temp()
    #     # a la temporal asignamos la posicion actual de P
    #     self.add_exp(t2, 'P', '1', '+')
    #     # anadir temporal que guardara la referencia del stack del numero ha convertir
    #     t3 = self.add_temp()
    #     self.get_stack(t3, t2)

    #     #########################
    #     # DECLARACION DE LABELS #
    #     #########################

    #     # Label para salir de la funcion
    #     return_lbl = self.new_label()
    #     # Label para iniciar el ciclo que convierte un numero ha string
    #     l1 = self.new_label()
    #     # Label para la creacion de un nuevo string
    #     l2 = self.new_label()

    #     ########################################################
    #     # CONVIRTIENDO NUEMRO HA STRING Y OBTENIENDO SU LENGTH #
    #     ########################################################

    #     # guardamos el incio de la nueva cadena
    #     self.add_comment(
    #         "INICIO DE LA NUEVA CADENA")
    #     t0 = self.add_temp()
    #     self.add_asig(t0, 'H')

    #     # creamos el temporal que se encargara de guardar el length del string que representa al numero
    #     t4 = self.add_temp()
    #     self.add_comment(
    #         "TEMPORAL QUE GUARDA EL LENGTH DE LA CADENA QUE REPRESENTA EL NUMERO A CONVERITR")
    #     # asignamos la t4 al length de la cadena que representa el numero t3
    #     self.add_asig(
    #         t4, f"float64(len(strconv.FormatFloat({t3}, 'f', -1, 64)))")

    #     # variable contadora que indicara cuantas iteraciones se han hecho
    #     t5 = self.add_temp()
    #     self.add_comment("TEMPORAL CONTADORA")
    #     # asignamos la t4 al length de la cadena que representa el numero t3
    #     self.add_asig(t5, f"0")

    #     #######################
    #     # INICIO DEL CICLO    #
    #     #######################

    #     # marcamos la label que inicia el ciclo
    #     self.put_label(l1)
    #     self.add_ident()
    #     # si la condatora es menor a la temporal que guarda el
    #     # length entonces mandamos ha guardar el caracter en la posicion de la contadora dentro del heap
    #     self.add_if(t5, t4, '<', l2)
    #     self.add_ident()
    #     # Si se encontro el -1 entonces debemos terminar el metodo
    #     self.add_if(t5, t4, '>=', return_lbl)

    #     ###############################
    #     # Acumulacion del contador    #
    #     ###############################

    #     self.put_label(l2)
    #     self.add_ident()
    #     # debemos guardar en una temporal la representacions Ascii del caracter posicionado en el contador
    #     t6 = self.add_temp()
    #     # guardar en una temporal la representacions Ascii del caracter posicionado en el contador
    #     self.add_asig(
    #         t6, f"float64(strconv.FormatFloat({t3}, 'f', -1, 64)[int({t5})])")
    #     self.add_ident()
    #     self.set_heap('H', t6)
    #     self.add_ident()
    #     self.next_heap()
    #     self.add_ident()
    #     # aumentamos un digito en la variable contadora
    #     self.add_exp(t5, t5, '1', '+')
    #     self.add_ident()
    #     # regresamos a la label que abre el ciclo
    #     self.add_goto(l1)

    #     ####################################
    #     # Declaracion del final del metodo #
    #     ####################################
    #     # declaramos la label que termina el metodo
    #     self.put_label(return_lbl)
    #     self.add_ident()
    #     # anadimos el caracter -1 a la nueva cadena
    #     self.set_heap('H', '-1')
    #     self.add_ident()
    #     # aumentamos en uno el heap
    #     self.next_heap()
    #     self.add_ident()
    #     # devolvemos la posicion inicial de la cadena
    #     self.set_stack('P', t0)
    #     self.add_end_func()
    #     self.in_natives = False

    def to_string_string(self):
        # if que reconoce si ya ha sido agregada la funcion to_string
        if self.to_string_stringg:
            return
        self.to_string_stringg = True
        self.in_natives = True

        # declaramos la nueva funcion to_string_number
        self.add_begin_func("to_string_string")
        # creamos una nueva temporal
        t2 = self.add_temp()
        # a la temporal asignamos la posicion actual de P
        self.add_exp(t2, 'P', '1', '+')
        # anadir temporal que guardara la referencia del stack del comienzo de la cadena ha convertir
        t3 = self.add_temp()
        self.get_stack(t3, t2)
        #########################
        # DECLARACION DE LABELS #
        #########################

        # Label para salir de la funcion
        return_lbl = self.new_label()
        # Label para iniciar el ciclo que convierte un numero ha string
        l1 = self.new_label()
        # Label para la creacion de un nuevo string
        l2 = self.new_label()

        ########################################################
        # CONVIRTIENDO NUEMRO HA STRING Y OBTENIENDO SU LENGTH #
        ########################################################

        # guardamos el incio de la nueva cadena
        self.add_comment(
            "INICIO DE LA NUEVA CADENA")
        t1 = self.add_temp()
        self.add_asig(t1, 'H')

        #######################
        # INICIO DEL CICLO    #
        #######################

        # marcamos la label que inicia el ciclo
        self.put_label(l1)
        # obtenemos el caracter de la primera cadena contenido en el heap
        t5 = self.add_temp()
        self.add_ident()
        self.get_heap(t5, t3)

        self.add_ident()

        # si la cadena es diferente de menos 1 entonces agregamos hacemos salto a la etiqueta que guarda la primera cadena
        self.add_if(t5, '-1', '!=', l2)
        self.add_ident()
        self.add_if(t5, '-1', '==', return_lbl)

        ##########################################
        # GUARDANDO CARACTERES EN NUEVA CADENA   #
        ##########################################

        self.put_label(l2)

        t6 = self.add_temp()
        self.add_ident()
        self.add_asig(t6, t5)
        self.add_ident()
        self.set_heap('H', t6)
        self.add_ident()
        self.next_heap()
        self.add_ident()
        # aumentamos un digito a la posicion a buscar en el heap
        self.add_exp(t3, t3, '1', '+')
        self.add_ident()
        # regresamos a la label que abre el ciclo
        self.add_goto(l1)

        ####################################
        # Declaracion del final del metodo #
        ####################################
        # declaramos la label que termina el metodo
        self.put_label(return_lbl)
        self.add_ident()
        # anadimos el caracter -1 a la nueva cadena
        self.set_heap('H', '-1')
        self.add_ident()
        # aumentamos en uno el heap
        self.next_heap()
        self.add_ident()
        # devolvemos la posicion inicial de la cadena
        self.set_stack('P', t1)
        self.add_end_func()
        self.in_natives = False

    def to_string_boolean(self):
        # if que reconoce si ya ha sido agregada la funcion to_string
        if self.to_string_booleann:
            return
        self.to_string_booleann = True
        self.in_natives = True

        # declaramos la nueva funcion to_string_number
        self.add_begin_func("to_string_boolean")
        # creamos una nueva temporal
        t2 = self.add_temp()
        # a la temporal asignamos la posicion actual de P
        self.add_exp(t2, 'P', '1', '+')
        # anadir temporal que guardara la referencia del stack del valor del booleano
        t3 = self.add_temp()
        self.get_stack(t3, t2)
        #########################
        # DECLARACION DE LABELS #
        #########################

        # Label para salir de la funcion
        return_lbl = self.new_label()
        # Label para iniciar el ciclo que convierte un numero ha string
        l1 = self.new_label()
        # Label para escribir true
        l2 = self.new_label()
        # label para escribir false
        l3 = self.new_label()

        ########################################################
        # CONVIRTIENDO NUEMRO HA STRING Y OBTENIENDO SU LENGTH #
        ########################################################

        # guardamos el incio de la nueva cadena
        self.add_comment(
            "INICIO DE LA NUEVA CADENA")
        t1 = self.add_temp()
        self.add_asig(t1, 'H')

        #######################
        # INICIO DEL CICLO    #
        #######################

        # marcamos la label que inicia el ciclo
        self.put_label(l1)
        self.add_ident()

        # si la cadena es diferente de menos 1 entonces agregamos hacemos salto a la etiqueta que guarda la primera cadena
        self.add_if(t3, '1', '==', l2)
        self.add_ident()
        self.add_if(t3, '0', '==', l3)

        ##########################################
        # GUARDANDO CARACTERES EN NUEVA CADENA   #
        ##########################################

        self.put_label(l2)

        self.add_ident()
        self.set_heap('H', '116')
        self.add_ident()
        self.next_heap()
        self.add_ident()
        self.set_heap('H', '114')
        self.add_ident()
        self.next_heap()
        self.add_ident()
        self.set_heap('H', '117')
        self.add_ident()
        self.next_heap()
        self.add_ident()
        self.set_heap('H', '101')
        self.add_ident()
        self.next_heap()
        self.add_ident()
        # regresamos a la label que abre el ciclo
        self.add_goto(return_lbl)

        ####################################
        # Declaracion del final del metodo #
        ####################################
        # declaramos la label que termina el metodo
        self.put_label(return_lbl)
        self.add_ident()
        # anadimos el caracter -1 a la nueva cadena
        self.set_heap('H', '-1')
        self.add_ident()
        # aumentamos en uno el heap
        self.next_heap()
        self.add_ident()
        # devolvemos la posicion inicial de la cadena
        self.set_stack('P', t1)
        self.add_end_func()
        self.in_natives = False

    def type_of_string(self):
        # if que reconoce si ya ha sido agregada la funcion to_string
        if self.type_of_stringg:
            return
        self.type_of_stringg = True
        self.in_natives = True

        # declaramos la nueva funcion to_string_number
        self.add_begin_func("type_of_string")
        # creamos una nueva temporal que guardara el inicio de la cadena
        t0 = self.add_temp()
        self.add_asig(t0, "H")

        # Escribimos caracter a caracter dentro del heap

        self.set_heap('H', '115')
        self.next_heap()
        self.set_heap('H', '116')
        self.next_heap()
        self.set_heap('H', '114')
        self.next_heap()
        self.set_heap('H', '105')
        self.next_heap()
        self.set_heap('H', '110')
        self.next_heap()
        self.set_heap('H', '103')
        self.next_heap()
        # anadimos el caracter -1 a la nueva cadena
        self.set_heap('H', '-1')
        # aumentamos en uno el heap
        self.next_heap()
        # devolvemos la posicion inicial de la cadena
        self.set_stack('P', t0)
        self.add_end_func()
        self.in_natives = False

    def type_of_number(self):
        # if que reconoce si ya ha sido agregada la funcion to_string
        if self.type_of_numberr:
            return
        self.type_of_numberr = True
        self.in_natives = True

        # declaramos la nueva funcion to_string_number
        self.add_begin_func("type_of_number")
        # creamos una nueva temporal que guardara el inicio de la cadena
        t0 = self.add_temp()
        self.add_asig(t0, "H")

        # Escribimos caracter a caracter dentro del heap

        self.set_heap('H', '110')
        self.next_heap()
        self.set_heap('H', '117')
        self.next_heap()
        self.set_heap('H', '109')
        self.next_heap()
        self.set_heap('H', '98')
        self.next_heap()
        self.set_heap('H', '101')
        self.next_heap()
        self.set_heap('H', '114')
        self.next_heap()
        # anadimos el caracter -1 a la nueva cadena
        self.set_heap('H', '-1')
        # aumentamos en uno el heap
        self.next_heap()
        # devolvemos la posicion inicial de la cadena
        self.set_stack('P', t0)
        self.add_end_func()
        self.in_natives = False

    def type_of_boolean(self):
        # if que reconoce si ya ha sido agregada la funcion to_string
        if self.type_of_booleann:
            return
        self.type_of_booleann = True
        self.in_natives = True

        # declaramos la nueva funcion to_string_number
        self.add_begin_func("type_of_boolean")
        # creamos una nueva temporal que guardara el inicio de la cadena
        t0 = self.add_temp()
        self.add_asig(t0, "H")

        # Escribimos caracter a caracter dentro del heap

        self.set_heap('H', '98')
        self.next_heap()
        self.set_heap('H', '111')
        self.next_heap()
        self.set_heap('H', '111')
        self.next_heap()
        self.set_heap('H', '108')
        self.next_heap()
        self.set_heap('H', '101')
        self.next_heap()
        self.set_heap('H', '97')
        self.next_heap()
        self.set_heap('H', '110')
        self.next_heap()
        # anadimos el caracter -1 a la nueva cadena
        self.set_heap('H', '-1')
        # aumentamos en uno el heap
        self.next_heap()
        # devolvemos la posicion inicial de la cadena
        self.set_stack('P', t0)
        self.add_end_func()
        self.in_natives = False

    def type_of_struct(self):
        # if que reconoce si ya ha sido agregada la funcion to_string
        if self.type_of_structt:
            return
        self.type_of_structt = True
        self.in_natives = True

        # declaramos la nueva funcion to_string_number
        self.add_begin_func("type_of_struct")
        # creamos una nueva temporal que guardara el inicio de la cadena
        t0 = self.add_temp()
        self.add_asig(t0, "H")

        # Escribimos caracter a caracter dentro del heap

        self.set_heap('H', '115')
        self.next_heap()
        self.set_heap('H', '116')
        self.next_heap()
        self.set_heap('H', '114')
        self.next_heap()
        self.set_heap('H', '117')
        self.next_heap()
        self.set_heap('H', '99')
        self.next_heap()
        self.set_heap('H', '116')
        self.next_heap()
        # anadimos el caracter -1 a la nueva cadena
        self.set_heap('H', '-1')
        # aumentamos en uno el heap
        self.next_heap()
        # devolvemos la posicion inicial de la cadena
        self.set_stack('P', t0)
        self.add_end_func()
        self.in_natives = False

    def p_out_of_bouns(self):
        if self.out_of_bouns:
            return
        label_out_program = self.new_label()
        self.label_out = label_out_program
        self.out_of_bouns = True
        self.in_natives = True
        self.add_begin_func('outOfBounds')
        error = "Acceso de array fuera de rango"
        for char in error:
            self.add_ident()
            self.add_print("c",ord(char))
        self.add_end_func()
        self.add_space()
        self.in_natives = False
    
    def to_exponential(self):
        pass
        ###############################
        # DEPRECADO POR INCUMPLIR C3D #
        ###############################


        # # if que reconoce si ya ha sido agregada la funcion to_exponential
        # if self.to_exponentiall:
        #     return
        # self.to_exponentiall = True
        # self.in_natives = True
        # # anadimos la libreria math para operaciones matematicas
        # self.set_import('math')
        # # anadimos la libreria math para operaciones matematicas
        # self.set_import('strconv')
        # # declaramos la nueva funcion to_string_number
        # self.add_begin_func("to_exponential")

        # ####################################################
        # # Variable que guarda el inicio de la nueva cadena #
        # ####################################################

        # t0 = self.add_temp()  # creamos la nueva temporal
        # # guardamos la posicion actua del hap antes demanipularlo
        # self.add_asig(t0, "H")

        # ###################################################################
        # #   Creacion de temporales que guardan el primer y segundo numero #
        # ###################################################################

        # # creamos una nueva temporal que guardara la poscion actual del Pointer
        # t1 = self.add_temp()
        # # a la temporal asignamos la posicion actual de P
        # self.add_exp(t1, 'P', '1', '+')
        # # Temporal que gurada el primer numero
        # t2 = self.add_temp()
        # # obtenemos el primer numero y lo guradamos en la temporal t2
        # self.get_stack(t2, t1)
        # # aumentamos el Ponter del Stack
        # self.add_exp(t1, t1, '1', '+')

        # # anadimos el temporal que gurada el segundo numero
        # t4 = self.add_temp()
        # self.get_stack(t4, t1)

        # ############################################
        # # Operaciones previas al inicio del blucle #
        # ############################################

        # # Temporal que guarda el resultado de hacer el pow 10 a la exponente
        # t5 = self.add_temp()
        # self.add_asig(
        #     t5, f"(math.Round({t2}*math.Pow(10, float64({t4}))) / math.Pow(10, float64({t4})))")
        # # # Temporal que guarda el resultado de multiplicar base * 10 ^exponente
        # # t6 = self.add_temp()
        # # self.add_asig(t6, f"float64({t2} * {t5})")

        # # Temporal que gurada el length de la cadena del resultado de la notacion cientifica
        # length_cadena_1 = self.add_temp()
        # self.add_asig(length_cadena_1,
        #               f"float64(len(strconv.FormatFloat({t5}, 'f', -1, 64)))")

        # # Temporal que gurarda el length del string del exponente
        # length_cadena_2 = self.add_temp()
        # self.add_asig(length_cadena_2,
        #               f"float64(len(strconv.FormatFloat({t4}, 'f', -1, 64)))")

        # # contadora del primer bucle
        # contadora_1 = self.add_temp()
        # self.add_asig(contadora_1, "0")
        # # contadora del segundo bucle bucle
        # contadora_2 = self.add_temp()
        # self.add_asig(contadora_2, "0")

        # #########################
        # # Declaracion de labels #
        # #########################

        # # label que inicia el bucle para la generacion de la cadena del primer bucle
        # bucle_1 = self.new_label()
        # # label que inicia el bucle para la generacion de la cadena del primer bucle
        # bucle_2 = self.new_label()
        # # label que inicia la acumulacion de una nueva cadena en el heap
        # creacion_cadena_1 = self.new_label()
        # # label que inicia la acumulacion de una nueva cadena en el heap
        # creacion_cadena_2 = self.new_label()
        # # label que inicia la acumulacion de una nueva cadena en el heap
        # creacion_cadena_e = self.new_label()
        # # label que termina el bucle
        # return_label = self.new_label()

        # #############################################################################################
        # # Inicio del bucle_1 que genera la primera cadena del resultado de hacer base * 10 ^exponente #
        # #############################################################################################

        # # anadimos la etiqueta del blucle
        # self.put_label(bucle_1)

        # self.add_ident()
        # # if que compara la variable contadora con le length de la cadena resultado de base * 10 ^exponente
        # self.add_if(contadora_1, length_cadena_1, "<", creacion_cadena_1)
        # self.add_ident()
        # self.add_if(contadora_1, length_cadena_1, ">=", creacion_cadena_e)

        # ###########################################################################
        # # Creacion de la nueva cadena representacion e+ #
        # ###########################################################################

        # self.put_label(creacion_cadena_e)
        # self.add_ident()
        # self.set_heap("H", "101")
        # self.add_ident()
        # self.next_heap()
        # self.add_ident()
        # self.set_heap("H", "43")
        # self.add_ident()
        # self.next_heap()
        # self.add_ident()
        # self.add_goto(bucle_2)

        # ###########################################################################
        # # Creacion de la nueva cadena representacion de  base * 10 ^exponente #
        # ###########################################################################

        # # anadir la label que inicia la creacion de la cadena
        # self.put_label(creacion_cadena_1)
        # self.add_ident()
        # # en el heap guardamos el caracter de la cadena en la pos contadora_1
        # self.set_heap(
        #     "H", f"float64(strconv.FormatFloat({t5}, 'f', -1, 64)[int({contadora_1})])")
        # self.add_ident()
        # self.next_heap()
        # self.add_ident()
        # # aumentamos la contadora_1
        # self.add_exp(contadora_1, contadora_1, "1", "+")
        # self.add_ident()
        # # regreamos a la etiqueta que comienza el primer loop
        # self.add_goto(bucle_1)

        # #############################################################################################
        # # Inicio del bucle_2 que genera la primera cadena del resultado de hacer base * 10 ^exponente #
        # #############################################################################################

        # # anadimos la etiqueta del blucle
        # self.put_label(bucle_2)

        # self.add_ident()
        # # if que compara la variable contadora con le length de la cadena resultado de base * 10 ^exponente
        # self.add_if(contadora_2, length_cadena_2, "<", creacion_cadena_2)
        # self.add_ident()
        # self.add_if(contadora_2, length_cadena_2, ">=", return_label)

        # ###########################################################################
        # # Creacion de la nueva cadena que representa el exponente enviado por el usuario#
        # ###########################################################################

        # # anadir la label que inicia la creacion de la cadena
        # self.put_label(creacion_cadena_2)
        # self.add_ident()
        # # en el heap guardamos el caracter de la cadena en la pos contadora_2
        # self.set_heap(
        #     "H", f"float64(strconv.FormatFloat({t4}, 'f', -1, 64)[int({contadora_2})])")
        # self.add_ident()
        # self.next_heap()
        # self.add_ident()
        # # aumentamos la contadora_1
        # self.add_exp(contadora_2, contadora_2, "1", "+")
        # self.add_ident()
        # # regreamos a la etiqueta que comienza el primer loop
        # self.add_goto(bucle_2)

        # #####################
        # # Fin de la funcion #
        # #####################

        # # anadimos la label que indica el fin de la funcion
        # self.put_label(return_label)
        # self.add_ident()
        # # colocamos el -1 en el heap
        # self.set_heap("H", "-1")
        # self.add_ident()
        # self.next_heap()
        # self.add_ident()
        # # devolvemos la posicion inicial de la cadena
        # self.set_stack('P', t0)
        # self.add_end_func()
        # self.in_natives = False
