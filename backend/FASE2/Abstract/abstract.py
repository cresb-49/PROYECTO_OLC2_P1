from abc import ABC, abstractclassmethod


class Abstract(ABC):
    def __init__(self, resultado, linea, columna):
        super().__init__()
        self.linea = linea
        self.columna = columna
        self.resultado = resultado
        # CODICO EXTRA PARA CODIGO 3 DIRECCIONES
        self.true_lbl = ''
        self.false_lbl = ''
        self.list_true_lbl = []
        self.list_false_lbl = []

    @abstractclassmethod
    def ejecutar(self, scope):
        pass

    @abstractclassmethod
    def graficar(self, graphviz, padre):
        pass

    @abstractclassmethod
    def generar_c3d(self, scope):
        pass

    def get_true_lbl(self):
        return self.true_lbl

    def get_false_lbl(self):
        return self.false_lbl

    def set_true_lbl(self, true_lbl):
        self.true_lbl = true_lbl

    def set_false_lbl(self, false_lbl):
        self.false_lbl = false_lbl
