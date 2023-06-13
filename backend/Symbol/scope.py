from Symbol.tipoEnum import TipoEnum


class Simbolo:
    def __init__(self, valor, id_, tipo, tipo_secundario, linea, columna):
        self.valor = valor
        self.id = id_
        self.tipo = tipo
        self.tipo_secundario = tipo_secundario
        self.linea = linea
        self.columna = columna

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

    def imprimir(self):
        for x in self.variables.get_diccionario():
            print('  ', self.variables.get_diccionario()[x])
        for x in self.funciones.get_diccionario():
            print('  ', self.funciones.get_diccionario()[x])

    def identificar(self, nombre, tipo):
        self.tipo = tipo
        self.nombre = nombre

    def reboot_variables(self):
        self.variables = Variables()

    def __str__(self) -> str:
        return f"Nombre: {self.nombre}, Tipo: {self.tipo}"

    def declarar_variable(self, id: str, valor: any, tipo, tipo_secundario, linea, columna):
        try:
            self.variables.add(id, Simbolo(
                valor, id, tipo, tipo_secundario, linea, columna))
        except ValueError as error:
            raise ValueError(str(error))

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
