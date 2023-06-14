from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum
from Symbol.scope import Scope

from Instrucciones.continuar import Continuar
from Instrucciones.detener import Detener


class Mientras(Abstract):
    def __init__(self, resultado, linea, columna, condicion, sentencias):
        super().__init__(resultado, linea, columna)
        self.condicion = condicion
        self.sentencias = sentencias

    def __str__(self):
        return f"While -> Condición: {self.condicion}, Sentencias: {self.sentencias}"

    def ejecutar(self, scope):
        codigo_referencia = str(id(self))
        result = self.condicion.ejecutar(scope)
        if result != None:
            if result['tipo'] == TipoEnum.BOOLEAN:
                try:
                    res: bool = result['value']
                    print('debuj mientras', res)
                    while res:
                        scope_temporal: Scope = Scope(scope)
                        # Registramos el scope generado
                        self.resultado.agregar_entorno(
                            codigo_referencia, scope_temporal)
                        if self.sentencias != None:
                            resultado = self.sentencias.ejecutar(
                                scope_temporal)
                            if isinstance(resultado, dict):
                                return resultado
                            elif isinstance(resultado, Continuar):
                                r = self.condicion.ejecutar(scope)
                                res = r['value']
                                # TODO: [IMPORTANTE] Eliminar debuj
                                print('debuj mientras:', resultado)
                            elif isinstance(resultado, Detener):
                                # TODO: [IMPORTANTE] Eliminar debuj
                                print('debuj mientras:', resultado)
                                break
                        r = self.condicion.ejecutar(scope)
                        res = r['value']
                except Exception as e:
                    # Toma el error de exception
                    print("Error:", str(e))
            else:
                self.resultado.add_error(
                    'Semantico', 'No se puede ejecutar la sentencia porque la condicional no es booleana', self.linea, self.columna)

        else:
            self.resultado.add_error(
                'Semantico', 'No se puede ejecutar la sentencia hay un error anterior', self.linea, self.columna)

    def graficar(self, graphviz, padre):
        mientras_node = graphviz.add_nodo('while', padre)
        self.condicion.graficar(graphviz, mientras_node)
        if (self.sentencias != None):
            self.sentencias.graficar(graphviz, mientras_node)
