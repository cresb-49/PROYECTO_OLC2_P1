from FASE2.Abstract.abstract import Abstract
from FASE2.Abstract.return__ import Return
from FASE2.Symbol.scope import Scope
from FASE2.Symbol.generador import Generador
from FASE2.Symbol.tipoEnum import TipoEnum

from FASE2.Instrucciones.declaracion import Declaracion
from FASE2.Instrucciones.asignacion import Asignacion
from FASE2.Instrucciones.detener import Detener
from FASE2.Instrucciones.continuar import Continuar
from FASE2.Nativas.length import Length

from FASE2.Expresiones.primitivo import Primitivo
from FASE2.Expresiones.aritmetica import Aritmetica
from FASE2.Expresiones.acceder import Acceder
from FASE2.Expresiones.acceder_array import AccederArray
from FASE2.Expresiones.arreglo import Arreglo
from FASE2.Expresiones.relacional import Relacional
from FASE2.Symbol.Exception import Excepcion

"""
tipo_for = 1 -> for (let i = 0; i < 10; i++) , declaracion, condicion, exprecion
tipo_for = 2 -> for (let var of var) , declaracion, exprecion
"""


class Para(Abstract):
    def __init__(self, resultado, linea, columna, tipo_for, declaracion, condicion, expresion, sentencias):
        super().__init__(resultado, linea, columna)
        self.tipo_for = tipo_for
        self.declaracion: Abstract = declaracion
        self.condicion: Abstract = condicion
        self.expresion: Abstract = expresion
        self.sentencias: Abstract = sentencias
        # RECUPERACION DE VARIABLES UTILIZADAS PARA GENERAR EL CODIGO EN 3 DIRECCIONES
        self.last_scope = None
        self.last_pre_scope_for = None
        self.last_inner_scope_for = None

    def __str__(self):
        attributes = []
        for attr, value in self.__dict__.items():
            attributes.append(f"{attr}: {type(value).__name__}={value}")
        return f"{type(self).__name__}: " + ", ".join(attributes)

    def ejecutar(self, scope):
        self.last_scope = scope
        codigo_referencia = str(id(self))
        if self.tipo_for == 1:
            # print('Ejecutamos for tipo 1')
            # Iniciamos un scope apartado del entorno del for
            scope_declarado_for: Scope = Scope(scope)
            self.last_pre_scope_for = scope_declarado_for
            # Registramos el entorno utilizado
            self.resultado.agregar_entorno(
                codigo_referencia, scope_declarado_for)
            # Declramos la variable asociada al for dentro del scope scope_declarado_for
            self.declaracion.ejecutar(scope_declarado_for)
            # Verificamos la exprecion condicional del for
            result = self.condicion.ejecutar(scope_declarado_for)
            if result != None:
                if result['tipo'] == TipoEnum.BOOLEAN:
                    try:
                        # res: bool = result['value']
                        # Eliminamos el uso while ya que solo vamos a inicializar lo valores del for
                        scope_temporal: Scope = Scope(scope_declarado_for)
                        self.last_inner_scope_for = scope_temporal
                        self.resultado.agregar_entorno(
                            codigo_referencia+'_sub2', scope_temporal)
                        if self.sentencias != None:
                            self.sentencias.ejecutar(scope_temporal)
                        self.expresion.ejecutar(scope_declarado_for)
                        # res = r['value']
                    except Exception as e:
                        # Toma el error de exception
                        print("Error:", str(e))
                else:
                    self.resultado.add_error(
                        'Semantico', 'No se puede ejecutar la sentencia porque la condicional no es booleana', self.linea, self.columna)

            else:
                self.resultado.add_error(
                    'Semantico', 'No se puede ejecutar la sentencia hay un error anterior', self.linea, self.columna)
        else:
            # print('Ejecutamos for tipo 2')
            # Iniciamos un scope apartado del entorno del for
            scope_declarado_for: Scope = Scope(scope)
            # Registramos el entorno utilizado
            self.resultado.agregar_entorno(
                codigo_referencia, scope_declarado_for)
            # Declramos la variable asociada al for dentro del scope scope_declarado_for
            result_expresion = self.expresion.ejecutar(scope_declarado_for)
            if result_expresion['tipo'] == TipoEnum.STRING or result_expresion['tipo'] == TipoEnum.ARRAY:
                # Generamos variables de ayuda para el ciclo
                # Contadores de acceso
                literal: Primitivo = Primitivo(
                    self.resultado, self.linea, self.columna, TipoEnum.NUMBER, float(0))
                maximo: Primitivo = Primitivo(
                    self.resultado, self.linea, self.columna, TipoEnum.NUMBER, float(len(result_expresion['value'])))
                contador: Declaracion = Declaracion(
                    self.resultado, self.linea, self.columna, '$contfor', TipoEnum.NUMBER, None, literal)
                limite: Declaracion = Declaracion(
                    self.resultado, self.linea, self.columna, '$maxfor', TipoEnum.NUMBER, None, maximo)
                op1: Acceder = Acceder(
                    self.resultado, self.linea, self.columna, '$contfor')
                op2: Primitivo = Primitivo(
                    self.resultado, self.linea, self.columna, TipoEnum.NUMBER, float(1))
                operacion: Aritmetica = Aritmetica(
                    self.resultado, self.linea, self.columna, op1, op2, '+')
                incrementar_valor: Asignacion = Asignacion(
                    self.resultado, self.linea, self.columna, '$contfor', operacion)
                if result_expresion['tipo'] == TipoEnum.ARRAY:
                    # print('for of de un array')
                    # print("estoy asignando Array")
                    var_arreglo: Declaracion = Declaracion(
                        self.resultado, self.linea, self.columna, '$valoresfor', TipoEnum.ARRAY, TipoEnum.ANY.value, self.expresion)
                    var_arreglo.ejecutar(scope_declarado_for)
                else:
                    # print('for of de un string')
                    lista = [caracter for caracter in result_expresion['value']]
                    arreglo_nuevo = []
                    for l in lista:
                        val: Primitivo = Primitivo(
                            self.resultado, self.linea, self.columna, TipoEnum.STRING, l)
                        arreglo_nuevo.append(val)
                    arr: Arreglo = Arreglo(
                        self.resultado, self.linea, self.columna, TipoEnum.ARRAY, None, arreglo_nuevo)
                    var_arreglo: Declaracion = Declaracion(
                        self.resultado, self.linea, self.columna, '$valoresfor', TipoEnum.ARRAY, TipoEnum.STRING.value, arr)
                    var_arreglo.ejecutar(scope_declarado_for)

                try:
                    self.declaracion.ejecutar(scope_declarado_for)
                    limite.ejecutar(scope_declarado_for)
                    contador.ejecutar(scope_declarado_for)

                    contador_for = Acceder(
                        self.resultado, self.linea, self.columna, '$contfor')
                    maximo_for = Acceder(
                        self.resultado, self.linea, self.columna, '$maxfor')
                    self.condicion = Relacional(
                        self.resultado, self.linea, self.columna, contador_for, maximo_for, '<')
                    result = self.condicion.ejecutar(scope_declarado_for)

                    name_var_for = self.declaracion.id
                    var_array = Acceder(
                        self.resultado, self.linea, self.columna, '$valoresfor')
                    index_array = Acceder(
                        self.resultado, self.linea, self.columna, '$contfor')
                    acceder_array = AccederArray(
                        self.resultado, self.linea, self.columna, var_array, index_array)
                    asignacion = Asignacion(
                        self.resultado, self.linea, self.columna, name_var_for, acceder_array)

                    while result['value']:
                        # print('debuj')
                        asignacion.ejecutar(scope_declarado_for)
                        scope_temporal: Scope = Scope(scope_declarado_for)
                        # Registramos el entorno utilizado
                        self.resultado.agregar_entorno(
                            codigo_referencia+'_sub2', scope_temporal)
                        if self.sentencias != None:
                            resultado = self.sentencias.ejecutar(
                                scope_temporal)
                            if isinstance(resultado, dict):
                                return resultado
                            elif isinstance(resultado, Detener):
                                break
                            elif isinstance(resultado, Continuar):
                                incrementar_valor.ejecutar(scope_declarado_for)
                        # Ejecuciones de final de ciclo
                        incrementar_valor.ejecutar(scope_declarado_for)
                        result = self.condicion.ejecutar(scope_declarado_for)
                except Exception as e:
                    print("Error:", str(e))

            else:
                self.resultado.add_error(
                    'Semantico', 'Solo se permiten iteraciones de array y string', self.linea, self.columna)

    def graficar(self, graphviz, padre):
        pass

    def generar_c3d(self, scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        if self.tipo_for == 1:
            generador.add_comment('Inicio de compilacion de ciclo for')
            # Genreacion de un scope intermedio
            pre_scope_for: Scope = Scope(scope)
            # Delaracion o acceso a la variable del ciclo
            self.declaracion.generar_c3d(pre_scope_for)
            # Generacion y colocaldo de la label de inicio del for
            label_intit = generador.new_label()
            generador.put_label(label_intit)
            # Generacion del codigo para la condicional del for y colocado de la etiqueta true
            ret: Return = self.condicion.generar_c3d(pre_scope_for)
            if (isinstance(ret, Excepcion)):
                return ret
            # Ingresamos la etiquetas para el sentencias de break y continue en la generacion del codigo intermedio
            for label in ret.get_false_lbls():
                pre_scope_for.add_break_label(label)
            pre_scope_for.admit_continue_label = True
            # print('labels ->', pre_scope_for)
            for label in ret.get_true_lbls():
                generador.put_label(label)
            # Generacion del codigo del las inttrucciones
            if self.sentencias != None:
                # Generacion de un inner scope para las sentencias dentro del for
                inner_scope_for: Scope = Scope(pre_scope_for)
                generador.add_comment('Instrucciones dentro del for')
                retr = self.sentencias.generar_c3d(inner_scope_for)
                if (isinstance(retr, Excepcion)):
                    return retr
                generador.add_comment('Fin instrucciones dentro del for')
            # Aqui se debe de agregar etiqueta del continue
            if pre_scope_for.continue_label != '':
                generador.put_label(pre_scope_for.continue_label)
            # Instrucciones del paso del for
            generador.add_comment('compilacion paso for')
            self.expresion.generar_c3d(pre_scope_for)
            generador.add_comment('fin compilacion paso for')
            # Instruccion de regreso a la condicional
            generador.add_goto(label_intit)
            # Generacion del final del ciclo for y lables de salida del ciclo
            for label in ret.get_false_lbls():
                generador.put_label(label)
            generador.add_comment('Fin de compilacion de ciclo for')
        else:
            generador.add_comment(
                'Inicio de compilacion de ciclo for iterable')
            # Generacion del scope interior del iterable
            pre_scope_for: Scope = Scope(scope)
            # Iniciamos el valor que se va a iterar
            valor_iterable: Return = self.expresion.generar_c3d(pre_scope_for)
            if isinstance(valor_iterable, Excepcion):
                return valor_iterable
            if valor_iterable.type == TipoEnum.STRING:
                self.for_string(valor_iterable, generador, pre_scope_for)
            elif valor_iterable.type == TipoEnum.ARRAY:
                print('iterable array')
            else:
                self.resultado.add_error(
                    'Semantico', 'Solo se permiten iteraciones de array y string', self.linea, self.columna)
                return Excepcion('Semantico', 'Solo se permiten iteraciones de array y string', self.linea, self.columna)
            generador.add_comment('Fin de compilacion de ciclo for iterable')

    def for_string(self, iterable: Return, generador: Generador, scope_pre_for: Scope):
        # print('Puntero del array', iterable)
        # Modificamos la variable declarada en el for
        self.declaracion.tipo = TipoEnum.STRING
        self.declaracion.tipo_secundario = None
        # Le agregamos un valor para que este se inicialice y tengamos un puntero del heap donde agregar el
        # valor de la cadena a iterar
        self.declaracion.valor = Primitivo(
            self.resultado, self.linea, self.columna, TipoEnum.STRING, '$')
        # Declaramos la variable en el scope especial enmedio del anterior y que esta dentro del for
        result_declaracion: Return = self.declaracion.generar_c3d(
            scope_pre_for)
        if isinstance(result_declaracion, Excepcion):
            return result_declaracion
        # Recuperamos la variable por medio de acceder para tener el puntero del heap
        accerder: Acceder = Acceder(
            self.resultado, self.linea, self.columna, self.declaracion.id)
        variable: Return = accerder.generar_c3d(scope_pre_for)
        if isinstance(variable, Excepcion):
            return variable
        # Recuperamos los puenteros para tener referencia de las cadenas
        puntero_variable = variable.get_value()
        puntero_string = iterable.get_value()
        # print('PUNTERO VARIABLE: ', puntero_variable)
        # print('PUNTERO STRING: ', puntero_string)
        # Variable para tener el puntero del heap
        temp_iterable = generador.add_temp()
        contador = generador.add_temp()
        generador.add_exp(contador, puntero_string, '0', '+')
        generador.add_comment('Inicio del iterable')
        true_label = generador.new_label()
        init_label = generador.new_label()
        false_label = generador.new_label()
        # Asignacion de las labels al scope del for
        scope_pre_for.add_break_label(false_label)
        scope_pre_for.admit_continue_label = True
        # Asignacion las labels dentro del ciclo
        generador.put_label(init_label)
        generador.get_heap(temp_iterable, contador)
        generador.set_heap(puntero_variable, temp_iterable)
        # Generacion de un scope para trabajo del for
        inner_scope: Scope = Scope(scope_pre_for)
        # Generacion del if
        generador.add_if(temp_iterable,'-1','!=',true_label)
        generador.add_goto(false_label)
        generador.put_label(true_label)
        # Sentencias del ciclo for
        if self.sentencias != None:
            ret: Return = self.sentencias.generar_c3d(inner_scope)
            if isinstance(ret, Excepcion):
                return ret
        # Aqui se debe de agregar etiqueta del continue
        if scope_pre_for.continue_label != '':
            generador.put_label(scope_pre_for.continue_label)
        generador.add_exp(contador, contador, '1', '+')
        generador.add_goto(init_label)
        generador.put_label(false_label)