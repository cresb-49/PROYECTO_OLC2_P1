class Pila:
    def __init__(self):
        self.items = []

    def esta_vacia(self):
        return len(self.items) == 0

    def apilar(self, elemento):
        self.items.append(elemento)

    def desapilar(self):
        if self.esta_vacia():
            return None
        return self.items.pop()

    def obtener_tamanio(self):
        return len(self.items)

    def obtener_tope(self):
        if self.esta_vacia():
            return None
        return self.items[-1]

    def limpiar(self):
        self.items = []

    def existe_elemento_abajo_arriba(self, dato):
        for item in self.items:
            if dato == item:
                return True
        return False

    def existe_elemento_arriba_abajo(self, dato):
        for item in reversed(self.items):
            if dato == item:
                return True
        return False
