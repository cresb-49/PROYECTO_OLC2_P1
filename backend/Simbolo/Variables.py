import Simbolo as Simbolo
from Abstracto.Tipo import Tipo

class Variables:
    def __init__(self):
        self.diccionario = {}

    def add(self, clave: str, valor: Simbolo):
        if clave in self.diccionario:
            raise ValueError(f"La funcion \"{str(clave)}\" ya esta definida en este scope")
        else:
            self.diccionario[clave] = valor

    def update(self, clave: str, valor: any, tipo: Tipo):
        if clave in self.diccionario:
            val = self.diccionario[clave]
            val.valor = valor
            val.tipo = tipo
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
