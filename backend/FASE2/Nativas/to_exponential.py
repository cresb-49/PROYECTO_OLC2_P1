from FASE2.Abstract.abstract import Abstract
from FASE2.Modulos.funcion_nativa import FuncionNativa
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Symbol.generador import Generador
from FASE2.Abstract.return__ import Return
from FASE2.Symbol.Exception import Excepcion

class ToExponential(Abstract):
    def __init__(self, resultado, linea, columna, numero, expreciones):
        super().__init__(resultado, linea, columna)
        self.tipo = TipoEnum.STRING
        self.expreciones = expreciones
        self.numero = numero

    def __str__(self):
        return "toExponential"

    def verificarTipos(self, val):
        # extremos el tipo de la variable
        tipo = val['tipo']
        if (tipo == TipoEnum.NUMBER):
            return True
        else:
            concat = f'Tipos no coinciden para la operacion toExponential(), Se esperaba String y recibio {tipo.value}'
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
                exponential = FuncionNativa.hacer_to_exponential(None, value_id, exponencial)
                #retornamos un nuevo diccionario con la informacion del fixed    
                return {"value": exponential, "tipo": TipoEnum.STRING, "tipo_secundario": None, "linea": self.linea, "columna": self.columna} 
            else:
                return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}  
        else:
            return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        # agregarmos el nombre del nodo (el de la operacion) y el nodo padre
        result = graphviz.add_nodo(".", padre)
        # mandmaos ha graficar os hijos
        self.numero.graficar(graphviz, result)
        node_expo = graphviz.add_nodo("toExponential", result)
        self.expreciones.graficar(graphviz, node_expo) 
    
    def generar_c3d(self,scope):
        
        c3d_numero : Return= self.numero.generar_c3d(scope)
        exponente: Return = self.expreciones.generar_c3d(scope)

        #verificamos los tipos del c3d para asegurarnos que la operacion se haga sobre numbers
        if(c3d_numero.get_tipo() != TipoEnum.NUMBER or exponente.get_tipo() != TipoEnum.NUMBER):
            return Excepcion("Semantico", "No se puede aplicar toExponential con valores no numerico", self.linea, self.columna)

        gen_aux = Generador()
        generador = gen_aux.get_instance()
        # envihamos ha generar la funcion de sumas
        generador.to_exponential()
        # generamos el primer temporal que guarda el valor del la base
        param_temp = generador.add_temp()
        generador.add_exp(param_temp, 'P', scope.size, '+')
        generador.add_exp(param_temp, param_temp, '1', '+')
        generador.set_stack(param_temp, c3d_numero.get_value())

        # asignamos el segundo valor que guarda el valor del exponente
        generador.add_exp(param_temp, param_temp, '1', '+')
        generador.set_stack(param_temp, exponente.get_value())

        # generar un nuevo entorno
        generador.new_env(scope.size)
        # llamamos a la funcion de sumar to_exponential
        generador.call_fun("to_exponential")

        # anadir un nuevo temporal que guardara el stack en P
        temp = generador.add_temp()
        generador.get_stack(temp, 'P')
        # retornamos el un entorno
        generador.ret_env(scope.size)

        generador.add_comment('Fin de la suma de to_exponential')
        generador.add_space()

        result = Return(temp, TipoEnum.STRING, False, None)

        return result