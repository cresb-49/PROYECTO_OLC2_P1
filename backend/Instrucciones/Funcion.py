import Abstracto.Instruccion as Instruccion


class Funcion(Instruccion):
    def ejecutar(self, scope) -> None:
        print("Ejecucion de la funcion")

    def graficar(self, scope, graphviz, padre) -> None:
        print("Graficacion de una funcion")
