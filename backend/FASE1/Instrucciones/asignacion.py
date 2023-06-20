from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum
from Symbol.generador import Generador


class Asignacion(Abstract):
    def __init__(self, resultado, linea, columna, id, valor):
        super().__init__(resultado, linea, columna)
        self.id = id
        self.valor = valor
        #CODIGO DE AYUDA REFERENCIA PARA LA EJECUCION
        self.resultado_valor = None
        self.last_scope = None

    def __str__(self):
        return f"Asignacion: {self.id}, Valor: {self.valor}"

    def ejecutar(self, scope):
        self.last_scope = scope
        # Ejecutamos lo que vamos a asignar a la variable
        result_exprecion = self.valor.ejecutar(scope)
        self.resultado_valor = result_exprecion
        # Buscamos la variable en el entorno/scope
        variable_recuperada = scope.obtener_variable(self.id)
        if variable_recuperada != None:
            # Verificamos una variable any ya que a esta le debemos cambiar su tipo secundario
            if variable_recuperada.tipo == TipoEnum.ANY:
                variable_recuperada.tipo_secundario = result_exprecion['tipo'].value
                variable_recuperada.valor = result_exprecion['value']
            else:
                # Verificamos que la variable recuperada coincida en tipo como es resultado de la exprecio
                if variable_recuperada.tipo == result_exprecion['tipo']:
                    variable_recuperada.valor = result_exprecion['value']
                else:
                    concat = f"No se puede asignar un: {result_exprecion['tipo'].value}, a la variable: {self.id}: {variable_recuperada.tipo.value} , linea: {self.linea}, columna: {self.columna}"
                    self.resultado.add_error(
                        'Semantico', concat, self.linea, self.columna)
        else:
            concat = 'No se puede encontrar la variable: ', self.id, ', linea: ', self.linea, ', columna: ', self.columna
            self.resultado.add_error(
                'Semantico', concat, self.linea, self.columna)

    def graficar(self, graphviz, padre):
        igual = graphviz.add_nodo('=', padre)
        graphviz.add_nodo(self.id, igual)
        self.valor.graficar(graphviz, igual)
    
    def generar_c3d(self,scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        # Recuperacion de la generacion de codigo 3 direcciones para la signacion del valor
        result = None
        if self.valor != None:
            result = self.valor.generar_c3d(scope)
        generador.add_comment(f'** compilacion de asignacion de variable {self.id} **')
        # Primero obtenermos la variable desde el scope generado por ultimo
        variable_recuperada = self.last_scope.obtener_variable(self.id)
        # Generamos dos variables temporales para el manejo de la informacion
        tempPos = variable_recuperada.simbolo_c3d.pos[4:]
        temp_Pos = variable_recuperada.simbolo_c3d.pos[4:]
        # Validacion si la varaible no es de tipo global
        if not variable_recuperada.simbolo_c3d.is_global:
            tempPos = generador.add_temp()
            generador.add_expression(tempPos, 'P', temp_Pos, '+')
        # si el resultado de asignacion es None entonces solo inicializamos con 0 la variable
        if result != None:
            generador.set_stack(tempPos, result.value)
        else:
            generador.set_stack(tempPos, 0)
        generador.add_comment(f'** fin de compilacion de asignacion variable {self.id} **')