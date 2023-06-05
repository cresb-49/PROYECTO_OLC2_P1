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
