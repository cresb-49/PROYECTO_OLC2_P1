from FASE2.Abstract.abstract import Abstract
from FASE2.Modulos.funcion_nativa import FuncionNativa
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Symbol.generador import Generador
from FASE2.Abstract.return__ import Return
from FASE2.Symbol.Exception import Excepcion

class ToFixed(Abstract):
    def __init__(self, resultado, linea, columna, numero, expreciones):
        super().__init__(resultado, linea, columna)
        self.expreciones = expreciones
        self.numero = numero

    def __str__(self):
        return "toFixed"

    def verificarTipos(self, val):
        # extremos el tipo de la variable
        tipo = val['tipo']
        if (tipo == TipoEnum.NUMBER):
            return True
        else:
            concat = f'Tipos no coinciden para la operacion toFixed(), Se esperaba String y recibio {tipo.value}'
            self.resultado.add_error(
                'Semantico', concat, self.linea, self.columna)
            return False

    def ejecutar(self, scope):
        # ejecutamos el diccionario del numero
        ejecutar = self.numero.ejecutar(scope)
        if(self.verificarTipos(ejecutar)):
            #Enviar ha ejecutar la exprecion para obtener su diccionario
            ejecutarExpresion = self.expreciones.ejecutar(scope)
            if(self.verificarTipos(ejecutarExpresion)):
                value_id = ejecutar['value'] #valor del id al que se aplico split
                exponencial = ejecutarExpresion['value'] #calor del saparador de split
                #mandamos ha ejecutar la funcion nativa con los valores recabados
                fixed = FuncionNativa.hacer_to_fixed(None, value_id, exponencial)
                #retornamos un nuevo diccionario con la informacion del fixed    
                return {"value": fixed, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna} 
            else:
                return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}  
        else:
            return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        # agregarmos el nombre del nodo (el de la operacion) y el nodo padre
        result = graphviz.add_nodo(".", padre)
        # mandmaos ha graficar os hijos
        self.numero.graficar(graphviz, result)
        node_fixed = graphviz.add_nodo("toFixed", result)
        self.expreciones.graficar(graphviz, node_fixed)
    
    def generar_c3d(self,scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()


        # mandamos ha traer el c3d de las expreciones que componen el fixed
        c3d_numero:Return = self.numero.generar_c3d(scope)
        c3d_expreciones:Return = self.expreciones.generar_c3d(scope)

        if(isinstance(c3d_numero, Excepcion) or isinstance(c3d_expreciones, Excepcion)):
            return c3d_numero


        #mandamos ha crear la funcion to fixed del generador
        generador.too_fixed()

        param_temp = generador.add_temp()
        generador.add_exp(param_temp,'P',scope.size,'+')

        #enviamos ha guardar el valor del primer valor (numero)
        generador.add_exp(param_temp,param_temp,'1','+')
        generador.set_stack(param_temp,c3d_numero.get_value())
        

        #seteamos en el stack el valor del segundo valor (expreciones)
        generador.add_exp(param_temp,param_temp,'1','+')
        generador.set_stack(param_temp,c3d_expreciones.get_value())
        
        #creacion del nuevo entorno
        generador.new_env(scope.size)

        #mandamos ha llamr a la funcion toFixed
        generador.call_fun("toFixed")
        
        temp = generador.add_temp()
        generador.get_stack(temp,'P')
        generador.ret_env(scope.size)
        

        
        #indicamos que se termino la compilacion de tofixed
        generador.add_comment('fin de to fixed')
        generador.add_space()

        result = Return(temp, TipoEnum.NUMBER, False, None)
        return result
        pass