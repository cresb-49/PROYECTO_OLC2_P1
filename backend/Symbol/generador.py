class Generador:
    generator = None
    def __init__(self) -> None:
        #Contadores
        self.count_temp = 0
        #Codigo
        self.codigo = ""
        #Lista de temporales
        self.temps = []
        #Lista de Naivas
        
        #TODO: Agregar la lista de nativas
        
        #Lista de imports
        self.imports = []
        self.imports2 = ['fmt','math']
    
    def get_instance(self):
        if Generador.generator == None:
            Generador.generator = Generador()
        return Generador.generator    
    
    def clean_all(self):
        #Contadores
        self.count_temp = 0
        #codigo
        self.codigo = ""
        #Lista de temporales
        self.temps = []
        #Lista de nativas
        
        self.imports = []
        self.imports2 = ['fmt','math']
        Generador.generator = Generador()
    
    #############
    # IMPORTS
    ############
    
    def set_import(self,lib):
        if lib in self.imports2:
            self.imports2.remove(lib)
        else:
            return 
        code = f'import(\n\t"{lib}"\n)\n'
    
     #############
    # CODE
    #############
    
    def get_header(self):
        code = '/* ---- HEADER ----- */\npackage main;\n\n'
        if len(self.imports) > 0:
            for temp in self.imports:
                code += temp
        if len(self.temps) > 0:
            code += 'var '
            for temp in self.temps:
                code += temp + ','
            code = code[:-1]
            code += " float64;\n\n"
        code += "var P, H float64;\nvar stack[30101999] float64;\nvar heap[30101999] float64;\n\n"

    def get_code(self):
        return f'{self.get_header()}\nfunc main(){{\n{self.codigo}\n}}'

    def add_comment(self, comment):
        self.codigo += f'/* {comment} */\n'
    
    def add_space(self):
        self.codigo += '\n'
    
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


    ###################
    # GOTO
    ###################


    ###################
    # IF
    ###################

    ###################
    # EXPRESIONES
    ###################
    
    def add_exp(self, result, left, right, op):
        self.codigo += f'{result} = {left} {op} {right};\n'
    
    def add_asig(self, result, left):
        self.codigo += f'{result} = {left};\n'
    
    ###############
    # STACK
    ###############

    def set_stack(self,pos, value):
        self.codigo += f'stack[int({pos})] = {value};\n'
    
    def get_stack(self, place, pos):
        self.codigo += f'{place} = stack[int({pos})];\n'
    
     #############
    # ENTORNO
    #############

    def new_env(self, size):
        self.codigo += '/* --- NUEVO ENTORNO --- */\n'
        self.codigo += f'P = P + {size};\n'
    
    def call_fun(self, id):
        self.codigo += f'{id}();\n'
    
    def ret_env(self, size):
        self.codigo += f'P = P - {size};\n'
        self.codigo += '/* --- RETORNO DE ENTORNO --- */\n'
        
    ###############
    # HEAP
    ###############

    def set_heap(self, pos, value):
        self.codigo += f'heap[int({pos})] = {value};\n'

    def get_heap(self, place, pos):
        self.codigo += f'{place} = heap[int({pos})];\n'

    def next_heap(self):
        self.codigo += 'H = H + 1;\n'
    
    ###############
    # INSTRUCCIONES
    ###############

    def add_print(self, type, value):
        self.set_import('fmt')
        self.codigo += f'fmt.Printf("%{type}", {value});\n' # %d %f %c %s