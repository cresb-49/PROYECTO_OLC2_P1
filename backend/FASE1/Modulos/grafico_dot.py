class GraficoDot():

    def __init__(self):
        self.declaraciones = []
        self.relaciones = []

    """
    Retorna el nodo que se agrego
    """

    def add_nodo(self,label, padre):
        id_ = len(self.declaraciones) + 1
        nombre_nodo = 'nodo' + str(id_)
        nodo: Nodo = Nodo(nombre_nodo, padre,label)
        self.declaraciones.append(nodo)
        return nodo

    def get_dot(self) -> str:
        result = ''
        definitions = ''
        for nodo in self.declaraciones:
            definitions = definitions + nodo.get_definicion() + "\n"
            result = result + nodo.get_relacion() + "\n"
        return ('digraph arbol {\n'+definitions + result+'}')


class Nodo():
    def __init__(self, nombre, pabre, label) -> None:
        self.nombre = nombre
        self.padre = pabre
        self.label = label

    def get_relacion(self):
        if (self.padre != None):
            return self.padre.nombre + ' -> ' + self.nombre 
        else:
            return ''

    def get_definicion(self):
        return self.nombre + f'[label="{self.label}"];'

#print('hola prueba')
#grafico: GraficoDot = GraficoDot()

#result = grafico.add_nodo('+',None)
#grafico.add_nodo('5',result)
#grafico.add_nodo('6',result)

#r = grafico.get_dot()
#print(r)
