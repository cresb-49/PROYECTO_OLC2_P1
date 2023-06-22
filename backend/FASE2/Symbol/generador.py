class Generador:
    generator = None

    def __init__(self) -> None:
        # Contadores
        self.count_temp = 0
        self.count_label = 0

        # Codigo
        self.codigo = ""
        self.funcs = ''
        self.natives = ''
        self.in_func = False
        self.in_natives = False

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

        # seteamos el pointer con el valor de la operacion to fixed
        self.set_stack(
            'P', f"math.Round({t3}*(math.Pow(10, float64({t4})))) / (math.Pow(10, float64({t4})))")

        self.add_end_func()
        self.in_natives = False

    def to_lower(self):
        if (self.to_lowerr):
            return
        # indicamos que se agrego una funcion toLower
        self.to_lowerr = True
        # indicamos que se creo una nativa
        self.in_natives = True
        # creamos la funcion toLowerCase
        self.add_begin_func('toLowerCase')
        # etiqueta de retorno
        return_et = self.new_label()
        # Etiqueta que permite la comparacion del valor del string
        compare_et = self.new_label()
        # temportal que guarda punteor al stack
        temp_p = self.add_temp()
        # termporal con puntero al heap
        temp_h = self.add_temp()
        # Se aumenta la posicion del stack en 1
        self.add_exp(temp_p, 'P', '1', '+')
        # Asignamos el un valor del stack en la posicion del heap
        self.get_stack(temp_h, temp_p)
        # temporal de comparacion
        temp_c = self.add_temp()
        self.put_label(compare_et)
        # movemos valor de heap ha stack
        self.get_heap(temp_c, temp_h)
        # Condicional que ientifica si el valor del stack es el valor de fin de cadena
        self.add_if(temp_c, '-1', '==', return_et)
        # Se agrega temporal
        temp = self.add_temp()
        # Se crea etiqueta de conversion
        pass_et = self.new_label()
        # If que excluye a los caracteres que no son minusculas
        self.add_if(temp_c, '65', '<', pass_et)
        self.add_if(temp_c, '90', '>', pass_et)
        # de no comporbarse los if entonces podemos aumentar en 32 el caracter
        self.add_exp(temp, temp_c, '32', '+')
        # guarda el valor de temporal en el heap
        self.set_heap(temp_h, temp)
        # agregar etiqueta de conversion
        self.put_label(pass_et)
        # Aumentar en 1 la posicion del heap
        self.add_exp(temp_h, temp_h, '1', '+')
        # Goto que inicializa las conficionales
        self.add_goto(compare_et)
        # Etiueta de salida del metodo
        self.put_label(return_et)
        # cerramos el metodo
        self.add_end_func()
        # Se desactiva flag que indica que se esta en una funcion nativa
        self.in_natives = False

    def to_upper(self):
        if (self.to_upperr):
            return
        self.to_upperr = True
        self.in_natives = True
        # creamos la funcion toUpperCase
        self.add_begin_func('toUpperCase')
        # etiqueta de retorno
        return_et = self.new_label()
        # Etiqueta que permite la comparacion del valor del string
        compare_et = self.new_label()
        # temportal que guarda punteor al stack
        temp_p = self.add_temp()
        # termporal con puntero al heap
        temp_h = self.add_temp()
        # Se aumenta la posicion del stack en 1
        self.add_exp(temp_p, 'P', '1', '+')
        # Asignamos el un valor del stack en la posicion del heap
        self.get_stack(temp_h, temp_p)
        # temporal de comparacion
        temp_c = self.add_temp()
        self.put_label(compare_et)
        # movemos valor de heap ha stack
        self.get_heap(temp_c, temp_h)
        # Condicional que ientifica si el valor del stack es el valor de fin de cadena
        self.add_if(temp_c, '-1', '==', return_et)
        # Se agrega temporal
        temp = self.add_temp()
        # Se crea etiqueta de conversion
        pass_et = self.new_label()
        # If que excluye a los caracteres que no son minusculas
        self.add_if(temp_c, '97', '<', pass_et)
        self.add_if(temp_c, '122', '>', pass_et)
        # de no comporbarse los if entonces podemos aumentar en 32 el caracter
        self.add_exp(temp, temp_c, '32', '-')
        # guarda el valor de temporal en el heap
        self.set_heap(temp_h, temp)
        # agregar etiqueta de conversion
        self.put_label(pass_et)
        # Aumentar en 1 la posicion del heap
        self.add_exp(temp_h, temp_h, '1', '+')
        # Goto que inicializa las conficionales
        self.add_goto(compare_et)
        # Etiueta de salida del metodo
        self.put_label(return_et)
        # cerramos el metodo
        self.add_end_func()
        # Se desactiva flag que indica que se esta en una funcion nativa
        self.in_natives = False

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
