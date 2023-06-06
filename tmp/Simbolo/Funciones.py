import Instrucciones.Funcion as Funcion


class Funciones:
    def __init__(self):
        self.diccionario = {}

    def add(self, clave: str, valor: Funcion):
        if clave in self.diccionario:
            raise ValueError(
                f"La variable \"{str(clave)}\" ya esta definida en este scope")
        else:
            self.diccionario[clave] = valor

    def has(self, clave: str) -> bool:
        return (clave in self.diccionario)

    def get(self, clave: str) -> Funcion:
        if clave in self.diccionario:
            return self.diccionario[clave]
        else:
            return None

    def delete(self, clave: str) -> None:
        if clave in self.diccionario:
            del self.diccionario["clave"]

    def get_diccionario(self):
        return self.diccionario
