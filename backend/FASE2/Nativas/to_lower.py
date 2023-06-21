from FASE2.Abstract.abstract import Abstract
from FASE2.Modulos.funcion_nativa import FuncionNativa
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Symbol.generador import Generador
from FASE2.Abstract.return__ import Return

class ToLowerCase(Abstract):

    def __init__(self, resultado, linea, columna, cadena):
        super().__init__(resultado, linea, columna)
        self.cadena = cadena

    def __str__(self):
        return "toLowerCase"

    def verificarTipos(self, val):
        # extremos el tipo de la variable
        tipo = val["tipo"]
        if (tipo == TipoEnum.STRING):
            return True
        else:
            concat = f'Tipos no coinciden para la operacion split(), Se esperaba String y recibio {tipo.value}'
            self.resultado.add_error(
                'Semantico', concat, self.linea, self.columna)
            return False

    def ejecutar(self, scope):
        # ejecutamos el diccionario
        ejecutar = self.cadena.ejecutar(scope)
        # una vez traida la variable debemos verificar que se trata d eun string
        if(self.verificarTipos(ejecutar)):
            # mandmaos ha hacer concat sobre el atributo value
            toString = FuncionNativa.hacer_to_lower_case(None, ejecutar['value'])
            # retornamos un diccionario con la String en lower y el tipo String
            return {"value": toString, "tipo": TipoEnum.STRING, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        else:
             # print('Debuj-> Primitivo ->', self)
            return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}



    def graficar(self, graphviz, padre):
        #agregarmos el nombre del nodo (el de la operacion) y el nodo padre
        result = graphviz.add_nodo(".", padre)
        #mandmaos ha graficar el hijo (acceder)
        self.numero.graficar(graphviz, result)
        graphviz.add_nodo("toLowerCase", result)

    def generar_c3d(self,scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()


        # mandamos ha traer el c3d de las expreciones que componen el fixed
        c3d_cadena:Return = self.cadena.generar_c3d(scope)
        #mandamos ha crear la funcion to fixed del generador
        generador.to_lower()

        param_temp = generador.add_temp()
        generador.add_exp(param_temp,'P',scope.size,'+')

        #enviamos ha guardar el valor del primer valor (numero)
        generador.add_exp(param_temp,param_temp,'1','+')
        generador.get_stack(param_temp,c3d_cadena.get_value())
        
        
        #creacion del nuevo entorno
        generador.new_env(scope.size)

        #mandamos ha llamr a la funcion toLowerCase
        generador.call_fun("toLowerCase")
        
        temp = generador.add_temp()
        generador.get_stack(temp,'P')
        generador.ret_env(scope.size)
        

        
        #indicamos que se termino la compilacion de tofixed
        generador.add_comment('fin de toLowerCase')
        generador.add_space()

        result = Return(temp, TipoEnum.STRING, False, None)
        return result