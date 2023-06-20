from FASE1.Symbol.tipoEnum import TipoEnum


class SimboloC3D:
    def __init__(self, in_heap):
        self.pos = 0  # Ubicacion en el stack
        self.is_global = False  # Sabemos si la variable es de tipo global
        self.in_heap = in_heap  # Si su valor esta contenido en el heap del programa
        self.value = None
        self.tipo_aux = ''
        self.length = 0
        self.referencia = False
        self.params = None

    def __str__(self):
        return f"Pos: {self.pos}, Is Global: {self.is_global}, In Heap: {self.in_heap}, Value: {self.value}, Tipo Aux: {self.tipo_aux}, Length: {self.length}, Referencia: {self.referencia}, Params: {self.params}"


class Simbolo:
    def __init__(self, valor, id_, tipo, tipo_secundario, linea, columna, simbolo_c3d):
        self.valor = valor
        self.id = id_
        self.tipo = tipo
        self.tipo_secundario = tipo_secundario
        self.linea = linea
        self.columna = columna
        self.simbolo_c3d = simbolo_c3d

    def __str__(self) -> str:
        return f"Variable: {self.id}, Tipo: {self.tipo}, Tipo_Secundario: {self.tipo_secundario}, Valor: {self.valor}, Línea: {self.linea}, Columna: {self.columna}"


class Scope:
    def __init__(self, anterior) -> None:
        self.anterior = anterior
        self.variables = Variables()
        self.funciones = Funciones()
        self.estructuras = Estructuras()
        self.nombre = id(self)
        self.tipo = ''
        # NUEVOS PARAMETROS PARA LA FASE 2
        self.size: int = 0
        if anterior != None:
            self.size = self.anterior.size

    def imprimir(self):
        for x in self.variables.get_diccionario():
            print('  ', self.variables.get_diccionario()[x])
        for x in self.funciones.get_diccionario():
            print('  ', self.funciones.get_diccionario()[x])
        for x in self.estructuras.get_diccionario():
            print('  ', self.estructuras.get_diccionario()[x])

    def identificar(self, nombre, tipo):
        self.tipo = tipo
        self.nombre = nombre

    def reboot_variables(self):
        self.variables = Variables()

    def __str__(self) -> str:
        return f"Nombre: {self.nombre}, Tipo: {self.tipo}"

    def declarar_variable(self, id: str, valor: any, tipo, tipo_secundario, linea, columna):
        try:
            # Calculo si los datos esta ubicados en el heap o en el stack
            # Lo hacemos por medio del tipo principal y secundario de la variable
            is_heap = False
            if tipo == TipoEnum.ARRAY or TipoEnum.STRING:
                is_heap = True
            # Generacion de parametros del simbolo en 3 direcciones
            simbolo_c3d: SimboloC3D = SimboloC3D(is_heap)
            new_symbol = Simbolo(
                valor, id, tipo, tipo_secundario, linea, columna, simbolo_c3d)
            self.variables.add(id, new_symbol)
            # Asignamos la direccion del stack a la variable ingresada
            variable = self.get_size()
            simbolo_c3d.pos = "pos_"+str(variable)
            # Aqui asignamos automaticamente si la variable a declarar es de tipo global
            if self.anterior == None:
                simbolo_c3d.is_global = True
        except ValueError as error:
            raise ValueError(str(error))

    def get_size(self):
        return self.size

    def sum_size(self):
        self.size += 1

    def modificar_variable(self, id: str, valor: any, tipo_secundario):
        if self.variables.has(id):
            self.variables.update(id, valor, tipo_secundario)
        else:
            raise ValueError(
                "No se modificar la variable porque no existe en el scope")

    def obtener_variable(self, id: str) -> any:
        scope = self
        while (scope != None):
            if (scope.variables.has(id)):
                return scope.variables.get(id)
            scope = scope.anterior
        return None

    def declarar_funcion(self, id: str, funcion):
        try:
            self.funciones.add(id, funcion)
        except ValueError as error:
            raise ValueError(str(error))

    def obtener_funcion(self, id: str):
        scope = self
        while (scope != None):
            if (scope.funciones.has(id)):
                return scope.funciones.get(id)
            scope = scope.anterior
        return None

    def declarar_estructura(self, id: str, estructura):
        try:
            self.estructuras.add(id, estructura)
        except ValueError as error:
            raise ValueError(str(error))

    def obtener_estructura(self, id: str):
        scope = self
        while (scope != None):
            if (scope.estructuras.has(id)):
                return scope.estructuras.get(id)
            scope = scope.anterior
        return None


class Variables:
    def __init__(self):
        self.diccionario = {}

    def add(self, clave: str, valor: Simbolo):
        if clave in self.diccionario:
            raise ValueError(
                f"La variable \"{str(clave)}\" ya esta definida en este scope")
        else:
            self.diccionario[clave] = valor

    def update(self, clave: str, valor: any, tipo_secundario):
        if clave in self.diccionario:
            val = self.diccionario[clave]
            val.valor = valor
            val.tipo_secundario = tipo_secundario
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


class Funciones:
    def __init__(self):
        self.diccionario = {}

    def add(self, clave: str, valor):
        if clave in self.diccionario:
            raise ValueError(
                f"Ya existe una Funcion \"{str(clave)}\" ya esta definida en programa")
        else:
            self.diccionario[clave] = valor

    def has(self, clave: str) -> bool:
        return (clave in self.diccionario)

    def get(self, clave: str):
        if clave in self.diccionario:
            return self.diccionario[clave]
        else:
            return None

    def delete(self, clave: str) -> None:
        if clave in self.diccionario:
            del self.diccionario["clave"]

    def get_diccionario(self):
        return self.diccionario


class Estructuras:
    def __init__(self):
        self.diccionario = {}

    def add(self, clave: str, valor):
        if clave in self.diccionario:
            raise ValueError(
                f"Ya existe un Struct \"{str(clave)}\" definido en el programa")
        else:
            self.diccionario[clave] = valor

    def has(self, clave: str) -> bool:
        return (clave in self.diccionario)

    def get(self, clave: str):
        if clave in self.diccionario:
            return self.diccionario[clave]
        else:
            return None

    def delete(self, clave: str) -> None:
        if clave in self.diccionario:
            del self.diccionario["clave"]

    def get_diccionario(self):
        return self.diccionario
